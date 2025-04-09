from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse
from .models import Book
from django.db.models import Exists, OuterRef, Q
from .models import Book, BookLoans, BookAuthors, Authors, Borrower
from .forms import BorrowerForm
from django.contrib import messages
import re
from django.core.paginator import Paginator
from django.db import connection
from datetime import date, datetime, timedelta


#-----------------------------------HomePage-----------------------------------------------------------------
def home(request):
    return render(request, 'library_app/index.html')

#-----------------------------------Search-------------------------------------------------------------------
def search_books(request):
    query = request.GET.get('q', '').strip()
    books = Book.objects.all().prefetch_related('authors')

    if query:
        books = books.filter(
            Q(isbn__icontains=query) |
            Q(title__icontains=query) |
            Q(authors__name__icontains=query)
        ).distinct()
        for book in books:
            book.is_available = book.is_book_available()
    else:
        books = []

    return render(request, "library_app/search.html", {"books": books, "query": query})


#----------------------------------Borrowers---------------------------------------------------------------
def generate_card_no():
    """
    Generate a new unique card number.
    """
    last_borrower = Borrower.objects.order_by('-card_id').first()
    
    if not last_borrower:
        return 'ID000001'
    
    last_card_no = last_borrower.card_id
    numeric_part = int(last_card_no[2:]) + 1
    return f'ID{numeric_part:06d}'

def create_borrower(request):
    if request.method == "POST":
        form = BorrowerForm(request.POST)
        if form.is_valid():
            borrower = form.save(commit=False)
            borrower.card_id = generate_card_no()
            borrower.save()

            messages.success(request, f"Borrower {borrower.bname} added successfully with Card ID {borrower.card_id}")
            return redirect('borrower_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BorrowerForm()

    return render(request, 'library_app/create_borrower.html', {'form': form})

def list_borrowers(request):
    """
    Display a list of borrowers.
    """
    borrowers = Borrower.objects.all()
    return render(request, 'library_app/borrower_list.html', {'borrowers': borrowers})

#-----------------------------------Book Loans-----------------------------------------------------------------
def run_query(query, params=None, fetch=True):
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        if fetch:
            return cursor.fetchall()

def check_in_out(request):
    context = {
        "checkout_msg": "",
        "checkin_results": [],
        "checkin_msg": "",
    }

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "checkout":
            isbn = request.POST.get("isbn")
            borrower_id = request.POST.get("borrower_id")

            if not isbn or not borrower_id:
                context["checkout_msg"] = "ISBN and Borrower ID are required."
            else:
                # Check if borrower exists
                borrower = run_query("SELECT card_id FROM BORROWER WHERE card_id = %s", [borrower_id])
                if not borrower:
                    context["checkout_msg"] = f"No borrower found with ID {borrower_id}."
                else:
                    # Check unpaid fines
                    fines = run_query("""
                        SELECT COUNT(*)
                        FROM FINES f JOIN BOOK_LOANS bl ON f.loan_id = bl.loan_id
                        WHERE bl.card_id = %s AND f.paid = false
                    """, [borrower_id])
                    if fines[0][0] > 0:
                        context["checkout_msg"] = f"Borrower {borrower_id} has unpaid fines."
                    else:
                        # Check number of active loans
                        loans = run_query("""
                            SELECT COUNT(*) FROM BOOK_LOANS
                            WHERE card_id = %s AND date_in IS NULL
                        """, [borrower_id])
                        if loans[0][0] >= 3:
                            context["checkout_msg"] = f"Borrower {borrower_id} has 3 active loans."
                        else:
                            # Check if book exists and is available
                            book = run_query("SELECT isbn FROM BOOK WHERE isbn = %s", [isbn])
                            if not book:
                                context["checkout_msg"] = f"Book with ISBN {isbn} not found."
                            else:
                                is_checked_out = run_query("""
                                    SELECT COUNT(*) FROM BOOK_LOANS
                                    WHERE isbn = %s AND date_in IS NULL
                                """, [isbn])
                                if is_checked_out[0][0] > 0:
                                    context["checkout_msg"] = f"Book {isbn} is already checked out."
                                else:
                                    due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
                                    run_query("""
                                        INSERT INTO BOOK_LOANS (card_id, isbn, date_out, due_date)
                                        VALUES (%s, %s, CURDATE(), %s)
                                    """, [borrower_id, isbn, due_date], fetch=False)
                                    context["checkout_msg"] = f"Book {isbn} checked out successfully to Borrower {borrower_id}."

        elif action == "checkin":
            search_type = request.POST.get("search_type")
            search_value = request.POST.get("search_value")
            if not search_value:
                context["checkin_msg"] = "Search value required."
            else:
                if search_type == "isbn":
                    results = run_query("""
                        SELECT bl.loan_id, bl.isbn, bl.card_id, bl.date_out, bl.due_date, bo.bname
                        FROM book_loans bl
                        JOIN book b ON bl.isbn = b.isbn
                        JOIN borrower bo ON bl.card_id = bo.card_id
                        WHERE bl.isbn = %s AND bl.date_in IS NULL
                    """, [search_value])
                elif search_type == "id":
                    results = run_query("""
                        SELECT bl.loan_id, bl.isbn, bl.card_id, bl.date_out, bl.due_date, bo.bname
                        FROM book_loans bl
                        JOIN book b ON bl.isbn = b.isbn
                        JOIN borrower bo ON bl.card_id = bo.card_id
                        WHERE bl.card_id = %s AND bl.date_in IS NULL
                    """, [search_value])
                else:  # name
                    results = run_query("""
                        SELECT bl.loan_id, bl.isbn, bl.card_id, bl.date_out, bl.due_date, br.bname
                        FROM book_loans bl
                        JOIN book b ON bl.isbn = b.isbn
                        JOIN borrower br ON bl.card_id = br.card_id
                        WHERE LOWER(br.bname) LIKE LOWER(%s) AND bl.date_in IS NULL
                    """, [f"%{search_value}%"])

                context["checkin_results"] = results
                if not results:
                    context["checkin_msg"] = "No outstanding loans found."

        elif action == "confirm_checkin":
            loan_ids = request.POST.getlist("loan_ids")
            for loan_id in loan_ids:
                run_query("""
                    UPDATE book_loans
                    SET date_in = CURDATE()
                    WHERE loan_id = %s
                """, [loan_id], fetch=False)
            context["checkin_msg"] = f"{len(loan_ids)} book(s) successfully checked in."

    return render(request, "library_app/check_in_out.html", context)

#-----------------------------------Fines-----------------------------------------------------------------
def calculate_fine(due_date, date_in):
    if isinstance(due_date, datetime):
        due_date = due_date.date()
    if date_in and isinstance(date_in, datetime):
        date_in = date_in.date()

    today = date.today()
    if date_in:
        days_late = (date_in - due_date).days
    else:
        days_late = (today - due_date).days

    return round(days_late * 0.25, 2) if days_late > 0 else 0.0

def run_query(query, params=None, fetch=True):
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        return cursor.fetchall() if fetch else None

def update_fines_view(request):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT loan_id, due_date, date_in
        FROM book_loans
        WHERE due_date < CURDATE()
    """)
    overdue_books = cursor.fetchall()

    for loan_id, due_date, date_in in overdue_books:
        cursor.execute("SELECT fine_amt, paid FROM fines WHERE loan_id = %s", [loan_id])
        existing = cursor.fetchone()

        calculated_fine = calculate_fine(due_date, date_in)

        if existing:
            fine_amt, paid = existing
            if not paid and calculated_fine != float(fine_amt):
                cursor.execute("UPDATE fines SET fine_amt = %s WHERE loan_id = %s", [calculated_fine, loan_id])
        else:
            if calculated_fine > 0:
                cursor.execute("INSERT INTO fines (loan_id, fine_amt, paid) VALUES (%s, %s, FALSE)", [loan_id, calculated_fine])

    connection.commit()
    return redirect("view_fines")

def view_fines(request):
    include_paid = request.GET.get("include_paid") == "true"
    search_borrower_id = request.GET.get("borrower_id")

    if search_borrower_id is None:
        search_borrower_id = ""

    query = """
        SELECT bl.card_id, SUM(f.fine_amt) as total_fine, MAX(f.paid) as is_paid
        FROM fines f
        JOIN book_loans bl ON f.loan_id = bl.loan_id
    """
    where_clause = []
    params = []

    if not include_paid:
        where_clause.append("f.paid = FALSE")

    if search_borrower_id:
        where_clause.append("bl.card_id = %s")
        params.append(search_borrower_id)

    if where_clause:
        query += " WHERE " + " AND ".join(where_clause)

    query += " GROUP BY bl.card_id"

    fines = run_query(query, params)
    message = request.GET.get('message', '')
    return render(request, "library_app/view_fines.html", {
        "fines": fines,
        "include_paid": include_paid,
        "message": message,
        "search_borrower_id": search_borrower_id,
    })

def pay_fine_view(request, card_id):
    if request.method == "POST":
        unpaid_fines = run_query("""
            SELECT f.loan_id
            FROM fines f
            JOIN book_loans bl ON f.loan_id = bl.loan_id
            WHERE bl.card_id = %s AND f.paid = FALSE
        """, [card_id])

        if not unpaid_fines:
            message = "No unpaid fines found for this borrower."
            return redirect(reverse("view_fines") + f"?message={message}")

        all_returned = True
        for loan_id, in unpaid_fines:
            date_in_result = run_query("SELECT date_in FROM book_loans WHERE loan_id = %s", [loan_id])
            if not date_in_result or not date_in_result[0][0]:
                all_returned = False
                break

        if not all_returned:
            message = "Cannot pay fines: some books have not been returned."
        else:
            for loan_id, in unpaid_fines:
                run_query("UPDATE fines SET paid = TRUE WHERE loan_id = %s", [loan_id], fetch=False)
            connection.commit()
            message = f"All fines paid successfully for borrower {card_id}."

        return redirect(reverse("view_fines") + f"?message={message}")

    return HttpResponse("Invalid request method.", status=405)
