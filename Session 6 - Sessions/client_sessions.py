from flask import (
    Flask,               # Core Flask class to create a Flask application instance
    render_template,      # Renders HTML templates
    redirect,             # Redirects the user to another route
    url_for,              # Dynamically builds URL for the specified endpoint
    flash,                # Displays one-time alert messages
    session,              # Manages user session data
    request               # Handles HTTP requests and retrieves form data
)
from forms import LoginForm  # Import the custom LoginForm class (likely defined in another file)

# Initialize the Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"  # Secret key used to manage sessions and securely sign cookies

# Route for the home page
@app.route("/")
@app.route("/home")  # Both "/" and "/home" will trigger this route
def home():
    # Renders the home.html template and passes the title "Home" to it
    return render_template("home.html", title="Home")

# Route for the about page
@app.route("/about")
def about():
    # Checks if the user is logged in by verifying if 'user_name' exists in the session
    if "user_name" not in session:
        flash("Login Required!")  # Shows a flash message if the user isn't logged in
        # Redirects the user to the login page and remembers the current page (request.url)
        return redirect(url_for('login', next=request.url))
    else:
        # If logged in, show a greeting message using the stored session username
        flash(f"Hi {session['user_name']}, have a good day!")
    # Render the about.html template and pass the title "About" to it
    return render_template("about.html", title="About")

# Route for the contact page
@app.route("/contact")
def contact():
    # Similar logic to the about page, checking if the user is logged in
    if "user_name" not in session:
        flash("Login Required!")
        return redirect(url_for('login', next=request.url))
    else:
        flash(f"Hi {session['user_name']}, have a good day!")
    # Render the contact.html template and pass the title "Contact"
    return render_template("contact.html", title="Contact")

# Route for the login page, allows both GET (show form) and POST (submit form) methods
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()  # Instantiate the login form
    # If the form is submitted and passes validation
    if form.validate_on_submit():
        # Store the username in the session to track the logged-in user
        session["user_name"] = form.username.data
        # Flash a success message using the session-stored username
        flash(f"Successfully logged in as {session['user_name'].title()}!")
        # Check if there's a 'next' URL, otherwise redirect to the home page
        next_url = request.args.get("next")
        return redirect(next_url or url_for("home"))
    # Render the login form if GET method or form validation fails
    return render_template("login.html", title="Login", form=form)

# Main execution point for the application
if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask app in debug mode (for development)
