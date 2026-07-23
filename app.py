from flask import Flask, render_template, request, redirect, session, Response
import sqlite3
import csv
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


app = Flask(__name__)

app.secret_key = "financehub_secret_key"



# Database connection

def get_db_connection():

    connection = sqlite3.connect("finance.db")

    return connection







# Home Page

@app.route("/")
def home():

    print("SESSION DATA:")
    print(session)

    return render_template("index.html")









# Register User

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":


        name = request.form["name"]

        email = request.form["email"]

        password = request.form["password"]



        connection = get_db_connection()

        cursor = connection.cursor()



        cursor.execute(
            """
            INSERT INTO users
            (name,email,password)

            VALUES(?,?,?)
            """,
            (
                name,
                email,
                password
            )
        )



        connection.commit()

        connection.close()



        return redirect("/login")



    return render_template("register.html")









# Login

@app.route("/login", methods=["GET","POST"])
def login():


    if request.method == "POST":


        email = request.form["email"]

        password = request.form["password"]



        connection = get_db_connection()

        cursor = connection.cursor()



        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email=? AND password=?
            """,
            (
                email,
                password
            )
        )



        user = cursor.fetchone()



        connection.close()



        if user:


            session["user_id"] = user[0]

            session["name"] = user[1]


            return redirect("/dashboard")



        else:

            return "Invalid Email or Password"



    return render_template("login.html")









# Logout

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
@app.route("/profile")
def profile():

    if "user_id" not in session:

        return redirect("/login")


    connection = get_db_connection()

    cursor = connection.cursor()



    # Get User Details

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id=?
        """,
        (session["user_id"],)
    )


    user = cursor.fetchone()



    # Count Transactions

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE user_id=?
        """,
        (session["user_id"],)
    )


    total_transactions = cursor.fetchone()[0]




    # Total Income

    cursor.execute(
        """
        SELECT SUM(amount)
        FROM transactions
        WHERE type='Income'
        AND user_id=?
        """,
        (session["user_id"],)
    )


    income = cursor.fetchone()[0] or 0





    # Total Expense

    cursor.execute(
        """
        SELECT SUM(amount)
        FROM transactions
        WHERE type='Expense'
        AND user_id=?
        """,
        (session["user_id"],)
    )


    expense = cursor.fetchone()[0] or 0




    balance = income - expense



    connection.close()



    return render_template(
        "profile.html",
        user=user,
        total_transactions=total_transactions,
        income=income,
        expense=expense,
        balance=balance
    )









# Dashboard

@app.route("/dashboard")
def dashboard():


    if "user_id" not in session:

        return redirect("/login")



    connection = get_db_connection()

    cursor = connection.cursor()





    # Get only current user's transactions

    cursor.execute(
        """
        SELECT *
        FROM transactions
        WHERE user_id=?
        """,
        (
            session["user_id"],
        )
    )


    transactions = cursor.fetchall()







    # Income

    cursor.execute(
        """
        SELECT SUM(amount)

        FROM transactions

        WHERE type='Income'
        AND user_id=?

        """,
        (
            session["user_id"],
        )
    )


    income = cursor.fetchone()[0] or 0







    # Expense

    cursor.execute(
        """
        SELECT SUM(amount)

        FROM transactions

        WHERE type='Expense'
        AND user_id=?

        """,
        (
            session["user_id"],
        )
    )


    expense = cursor.fetchone()[0] or 0





    balance = income - expense








    # Expense Pie Chart Data

    cursor.execute(
        """
        SELECT category, SUM(amount)

        FROM transactions

        WHERE type='Expense'
        AND user_id=?

        GROUP BY category

        """,
        (
            session["user_id"],
        )
    )


    expense_data = cursor.fetchall()



    connection.close()





    return render_template(
        "dashboard.html",

        transactions=transactions,

        income=income,

        expense=expense,

        balance=balance,

        expense_data=expense_data
    )









# Add Transaction

@app.route("/add", methods=["GET","POST"])
def add_transaction():


    if "user_id" not in session:

        return redirect("/login")



    if request.method == "POST":


        date = request.form["date"]

        category = request.form["category"]

        transaction_type = request.form["type"]

        amount = int(request.form["amount"])





        connection = get_db_connection()

        cursor = connection.cursor()




        cursor.execute(
            """
            INSERT INTO transactions

            (date,category,type,amount,user_id)

            VALUES(?,?,?,?,?)

            """,
            (
                date,

                category,

                transaction_type,

                amount,

                session["user_id"]
            )
        )



        connection.commit()

        connection.close()



        return redirect("/dashboard")




    return render_template("add_transaction.html")











# Edit Transaction

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit_transaction(id):


    if "user_id" not in session:

        return redirect("/login")



    connection = get_db_connection()

    cursor = connection.cursor()




    if request.method == "POST":


        date = request.form["date"]

        category = request.form["category"]

        transaction_type = request.form["type"]

        amount = int(request.form["amount"])




        cursor.execute(
            """
            UPDATE transactions

            SET date=?,
            category=?,
            type=?,
            amount=?

            WHERE id=?
            AND user_id=?

            """,
            (
                date,

                category,

                transaction_type,

                amount,

                id,

                session["user_id"]
            )
        )



        connection.commit()

        connection.close()



        return redirect("/dashboard")






    cursor.execute(
        """
        SELECT *

        FROM transactions

        WHERE id=?

        AND user_id=?

        """,
        (
            id,

            session["user_id"]
        )
    )



    transaction = cursor.fetchone()



    connection.close()



    return render_template(
        "edit_transaction.html",

        transaction=transaction
    )
    









# Delete Transaction

@app.route("/delete/<int:id>")
def delete_transaction(id):


    if "user_id" not in session:

        return redirect("/login")



    connection = get_db_connection()

    cursor = connection.cursor()



    cursor.execute(
        """
        DELETE FROM transactions

        WHERE id=?

        AND user_id=?

        """,
        (
            id,

            session["user_id"]
        )
    )



    connection.commit()

    connection.close()



    return redirect("/dashboard")

 # About Page
@app.route("/about")
def about():
    return render_template("about.html")


# Contact Page
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/export")
def export_csv():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT date, category, type, amount
        FROM transactions
        WHERE user_id=?
    """, (session["user_id"],))

    transactions = cursor.fetchall()

    connection.close()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow(["Date", "Category", "Type", "Amount"])

    for row in transactions:
        writer.writerow(row)

    csv_data = output.getvalue()

    output.close()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=transactions.csv"
        }
    )
 # Export Transactions as PDF

@app.route("/export-pdf")
def export_pdf():

    if "user_id" not in session:
        return redirect("/login")


    connection = get_db_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT date, category, type, amount
        FROM transactions
        WHERE user_id=?
        """,
        (session["user_id"],)
    )


    transactions = cursor.fetchall()


    connection.close()



    buffer = io.BytesIO()


    pdf = canvas.Canvas(buffer, pagesize=letter)


    pdf.setTitle("FinanceHub Transactions")


    pdf.drawString(
        200,
        750,
        "FinanceHub Transaction Report"
    )


    y = 700


    pdf.drawString(
        50,
        y,
        "Date"
    )

    pdf.drawString(
        150,
        y,
        "Category"
    )

    pdf.drawString(
        280,
        y,
        "Type"
    )

    pdf.drawString(
        380,
        y,
        "Amount"
    )


    y -= 30



    for transaction in transactions:


        pdf.drawString(
            50,
            y,
            str(transaction[0])
        )


        pdf.drawString(
            150,
            y,
            str(transaction[1])
        )


        pdf.drawString(
            280,
            y,
            str(transaction[2])
        )


        pdf.drawString(
            380,
            y,
            "₹" + str(transaction[3])
        )


        y -= 25



        if y < 50:

            pdf.showPage()

            y = 750



    pdf.save()



    buffer.seek(0)



    return Response(
        buffer,
        mimetype="application/pdf",
        headers={
            "Content-Disposition":
            "attachment;filename=transactions.pdf"
        }
    )   
    # GST Calculator

@app.route("/gst", methods=["GET","POST"])
def gst():

    gst_amount = None
    total_amount = None


    if request.method == "POST":


        amount = float(request.form["amount"])

        gst_percentage = float(request.form["gst"])


        gst_amount = amount * gst_percentage / 100


        total_amount = amount + gst_amount



    return render_template(
        "gst.html",
        gst_amount=gst_amount,
        total_amount=total_amount
    )
    # EMI Calculator

@app.route("/emi")
def emi():

    return render_template("emi.html")
# SIP Calculator

@app.route("/sip")
def sip():

    return render_template("sip.html")
# Profit and Loss Calculator

@app.route("/profit-loss")
def profit_loss():

    return render_template("profit_loss.html")





# Invoice Generator

@app.route("/invoice")
def invoice():

    return render_template("invoice.html")




if __name__ == "__main__":

    app.run(debug=True)