from django.db import models

# Authors model
class Authors(models.Model):
    author_id = models.AutoField(db_column='Author_id', primary_key=True)
    name = models.CharField(db_column='Name', max_length=255)

    class Meta:
        managed = False
        db_table = 'authors'

# Book model
class Book(models.Model):
    isbn = models.CharField(db_column='Isbn', primary_key=True, max_length=13)
    title = models.CharField(db_column='Title', max_length=500)
    authors = models.ManyToManyField(Authors, through='BookAuthors')

    def is_book_available(self):
        return not self.bookloans_set.filter(date_in__isnull=True).exists()

    class Meta:
        managed = False
        db_table = 'book'

# BookAuthors model
class BookAuthors(models.Model):
    author = models.ForeignKey(Authors, models.DO_NOTHING, db_column='Author_id')
    isbn = models.ForeignKey(Book, models.DO_NOTHING, db_column='Isbn')

    class Meta:
        managed = False
        db_table = 'book_authors'

# BookLoans model
class BookLoans(models.Model):
    loan_id = models.AutoField(db_column='Loan_id', primary_key=True)
    isbn = models.ForeignKey(Book, models.DO_NOTHING, db_column='Isbn', blank=True, null=True)
    card = models.ForeignKey('Borrower', models.DO_NOTHING, db_column='Card_id', blank=True, null=True)
    date_out = models.DateTimeField(db_column='Date_out', blank=True, null=True)
    due_date = models.DateTimeField(db_column='Due_date', blank=True, null=True)
    date_in = models.DateTimeField(db_column='Date_in', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_loans'

# Borrower model
class Borrower(models.Model):
    card_id = models.CharField(db_column='Card_id', primary_key=True, max_length=10)
    ssn = models.CharField(db_column='Ssn', unique=True, max_length=11, blank=True, null=True)
    bname = models.CharField(db_column='Bname', max_length=255)
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)
    phone = models.CharField(db_column='Phone', max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'borrower'

# Fines model
class Fines(models.Model):
    loan = models.OneToOneField(BookLoans, models.DO_NOTHING, db_column='Loan_id', primary_key=True)
    fine_amt = models.DecimalField(db_column='Fine_amt', max_digits=10, decimal_places=2, blank=True, null=True)
    paid = models.IntegerField(db_column='Paid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fines'
