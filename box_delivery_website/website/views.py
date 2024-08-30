from math import prod
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


chrome_Options = Options()
#chrome_Options.add_argument("--headless")
PATH = r"chromedriver.exe"
CHROME_PATH = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
chrome_Options.binary_location = CHROME_PATH

views = Blueprint('views', __name__)
from bs4 import BeautifulSoup
import requests

# Function to extract Product Title
def get_title(soup):
	
	try:
		# Outer Tag Object
		title = soup.find("span", attrs={"id":'productTitle'})
		print(type(title))

		# Inner NavigableString Object
		title_value = title.string
		print(type(title_value))

		# Title as a string value
		title_string = title_value.strip()
		print(type(title_string))

		# # Printing types of values for efficient understanding
		print()

	except AttributeError:
		title_string = ""	

	return title_string

# Function to extract Product Price
def get_price(soup):

	try:
		price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

	except AttributeError:
		price = ""	

	return price

# Function to extract Product Rating
def get_rating(soup):

	try:
		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
		
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
	try:
		review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
		
	except AttributeError:
		review_count = ""	

	return review_count

# Function to extract Availability Status
def get_availability(soup):
	try:
		available = soup.find("div", attrs={'id':'availability'})
		available = available.find("span").string.strip()

	except AttributeError:
		available = ""	

	return available	

amazonWebsite = "amazon.com"
def checkBoxSize(length, width, height, weight):
    size = "none"
    if weight > 20:
        return "package is too heavy for international mailing"

    if length <= 8.62 and width <= 5.37 and height <= 1.62:
        size = "small"
        if weight > 4:
            size = "medium"
    elif ((length <= 13.62 and length > 8.62) and (width <= 11.87 and width > 5.37) and (height <= 3.37)) or ((length <= 11 and length > 8.62) and (width <= 8.5 and width > 5.37) and (height <= 5.5)):
        size = "medium"
    elif ((length <= 23.68 and length > 13.62) and (width <= 11.75) and (height <= 3)) or ((length <= 12 and length > 8.62) and (width <= 12 and width > 5.37) and (height <= 5.5)):
        size = "large"
    else:
        size = "too large for international mailing"

    return size

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if amazonWebsite in note:
            # Headers for request
            HEADERS = ({'User-Agent':
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                        'Accept-Language': 'en-US, en;q=0.5'})

            # The webpage URL
            URL = note

            # HTTP Request
            webpage = requests.get(URL, headers=HEADERS)

        	# Soup Object containing all data
            soup = BeautifulSoup(webpage.content, "lxml")
            #productTitle = openDrive.find_element_by_xpath((f"//div[@id='titleSection']/h1/span[@id='productTitle']"))
            #productPrice = openDrive.find_element_by_xpath((f"//div[@id='buybox']/div[contains('$')]"))
            #productDimension = openDrive.find_element_by_xpath((f"//div[@class='a-section table-padding']/table/tbody/tr[6]/td"))
            #productWeight = openDrive.find_element_by_xpath((f"//div[@class='a-section table-padding']/table/tbody/tr[10]/td"))
            #productPriceSplit = productPrice.text.split('$')[1]
            shippingPrice = "10.00"
            #productTax = (float(productPriceSplit)+float(shippingPrice)) * 0.065
            #totalPrice = (float(productPriceSplit)+float(shippingPrice)+float(productTax))
            
            # ADD TO CART AND SUM ALL PRODUCTS IN CART
            #return render_template("cart.html", user=current_user)
            #flash(productTitle.text, category='success')
            #flash(f"price: {productPrice.text}", category='success')
            #flash(f"package dimensions: length: {productDimension.text.split()[0]} width: {productDimension.text.split()[2]} height: {productDimension.text.split()[4]}", category='success')
            #flash(f"weight: {productWeight.text.split()[0]}", category='success')
            #flash(f"amazon shipping: ${shippingPrice}", category='success')
            #flash(f"tax: ${round(productTax,2)}", category='success')
            #flash(f"product total: ${round(totalPrice,2)}", category='success')
            #flash(f"international mailing: {checkBoxSize(float(productDimension.text.split()[0]), float(productDimension.text.split()[2]), float(productDimension.text.split()[4]), float(productWeight.text.split()[0]))}", category='success')
            #flash(f"delivery to brasil fee: ${round(totalPrice*0.30,2)}", category='success')
            #flash(f"total: ${round(totalPrice+(totalPrice*0.30),2)}", category='success')
            # Function calls to display all necessary product information
            print("Product Title =", get_title(soup))
            print("Product Price =", get_price(soup))
            print("Product Rating =", get_rating(soup))
            print("Number of Product Reviews =", get_review_count(soup))
            print("Availability =", get_availability(soup))
        else:
            flash('Invalid Website!', category='error')


    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
