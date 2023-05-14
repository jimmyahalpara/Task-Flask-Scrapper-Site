from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import numpy as np 
import pandas as pd 
import requests
import multiprocessing as mp
# from app import db, Product
import time


app = Flask(__name__)
# connection to mysql database using password NO
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/scrapper'

db = SQLAlchemy(app)

class ApplicationState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # key column with index
    key = db.Column(db.String(80), index=True, nullable=False)
    # text column
    value = db.Column(db.String(300), nullable=False)
class MainConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # key column with index 
    key = db.Column(db.String(80), index=True, nullable=False)
    # text column
    value = db.Column(db.String(300), nullable=False)

class RunTimeConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # key column with index 
    key = db.Column(db.String(80), index=True, nullable=False)
    # text column
    value = db.Column(db.String(300), nullable=False)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # sku column as index (not unique) 
    sku = db.Column(db.String(80), index=True, nullable=False)

    company_price = db.Column(db.Float, nullable=True)

    contractor_1 = db.Column(db.String(80), nullable=True)
    price_1 = db.Column(db.Float, nullable=True)
    has_sale_1 = db.Column(db.String(5), nullable=True)
    
    contractor_2 = db.Column(db.String(80), nullable=True)
    price_2 = db.Column(db.Float, nullable=True)
    has_sale_2 = db.Column(db.String(5), nullable=True)

    contractor_3 = db.Column(db.String(80), nullable=True)
    price_3 = db.Column(db.Float, nullable=True)
    has_sale_3 = db.Column(db.String(5), nullable=True)

    contractor_4 = db.Column(db.String(80), nullable=True)
    price_4 = db.Column(db.Float, nullable=True)
    has_sale_4 = db.Column(db.String(5), nullable=True)

    contractor_5 = db.Column(db.String(80), nullable=True)
    price_5 = db.Column(db.Float, nullable=True)
    has_sale_5 = db.Column(db.String(5), nullable=True)

    contractor_6 = db.Column(db.String(80), nullable=True)
    price_6 = db.Column(db.Float, nullable=True)
    has_sale_6 = db.Column(db.String(5), nullable=True)

    contractor_7 = db.Column(db.String(80), nullable=True)
    price_7 = db.Column(db.Float, nullable=True)
    has_sale_7 = db.Column(db.String(5), nullable=True)

    contractor_8 = db.Column(db.String(80), nullable=True)
    price_8 = db.Column(db.Float, nullable=True)
    has_sale_8 = db.Column(db.String(5), nullable=True)

    contractor_9 = db.Column(db.String(80), nullable=True)
    price_9 = db.Column(db.Float, nullable=True)
    has_sale_9 = db.Column(db.String(5), nullable=True)

    contractor_10 = db.Column(db.String(80), nullable=True)
    price_10 = db.Column(db.Float, nullable=True)
    has_sale_10 = db.Column(db.String(5), nullable=True)

    # int column 
    is_completed = db.Column(db.Integer, nullable=True)
    # text column
    error_message = db.Column(db.String(300), nullable=True)


    def __repr__(self):
        return '<Product %r>' % self.sku
    def to_dict(self):
        return {
            'sku': self.sku,
            'Company Price': self.company_price,
            '1st Rank': self.contractor_1,
            'price 1': self.price_1,
            'has sale 1': self.has_sale_1,
            '2nd Rank': self.contractor_2,
            'price 2': self.price_2,
            'has sale 2': self.has_sale_2,
            '3rd Rank': self.contractor_3,
            'price 3': self.price_3,
            'has sale 3': self.has_sale_3,
            '4th Rank': self.contractor_4,
            'price 4': self.price_4,
            'has sale 4': self.has_sale_4,
            '5th Rank': self.contractor_5,
            'price 5': self.price_5,
            'has sale 5': self.has_sale_5,
            '6th Rank': self.contractor_6,
            'price 6': self.price_6,
            'has sale 6': self.has_sale_6,
            '7th Rank': self.contractor_7,
            'price 7': self.price_7,
            'has sale 7': self.has_sale_7,
            '8th Rank': self.contractor_8,
            'price 8': self.price_8,
            'has sale 8': self.has_sale_8,
            '9th Rank': self.contractor_9,
            'price 9': self.price_9,
            'has sale 9': self.has_sale_9,
            '10th Rank': self.contractor_10,
            'price 10': self.price_10,
            'has sale 10': self.has_sale_10,
        }
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset():
    # truncate Product table
    Product.query.delete()
    # commit the changes
    db.session.commit()
    # return as json

    # update application state to 0
    state = ApplicationState.query.filter_by(key='application_state_code').first()
    # set value to 0
    state.value = '0'
    # commit the changes
    db.session.commit()
    return {
        'status': 'success'
    }

@app.route('/output-files')
def output_files():
    # get all the file list with last modified datetime 
    import os
    from datetime import datetime
    files = []
    for file in os.listdir("static/output"):
        files.append({
            'name': file,
            'last_modified': datetime.fromtimestamp(os.path.getmtime("static/output/" + file)).strftime("%Y-%m-%d %H:%M:%S"),
            # if the last modified date is less than 1 hr, then term it as new 
            'is_new': True if (datetime.now() - datetime.fromtimestamp(os.path.getmtime("static/output/" + file))).total_seconds() < 300 else False
        })
    # return as json 
    # reverset the list 
    files.reverse()
    return {
        'files': files
    }

# delete all files 
@app.route('/delete-files', methods=['POST'])
def delete_files():
    import os, shutil
    # delete all files from static/output folder
    shutil.rmtree('static/output')
    # create a new folder
    os.mkdir('static/output')
    # return as json 
    return {
        'status': 'success'
    }

@app.route('/progress')
def progress():
    # check data from Product table
    # get list of product with is_completed = 0 and is_completed != 0 
    # get count of both
    # return as json

    compelted = Product.query.filter(Product.is_completed != 0).count()
    total = Product.query.count()
    # is_completed_0 = Product.query.filter(Product.is_completed == 0).count()


    # get all rows from ApplicationState table
    application_state = ApplicationState.query.all()
    # print(application_state)
    # set key as index
    application_state = {row.key: row.value for row in application_state}
    # application_state['application_state_code'] = 1;

    # last modified file from status/output 
    return {
        'completed': compelted,
        'total' : total,
        'progress': round((compelted / total) * 100, 2) if total > 0 else 0,
        'status': 'completed' if (compelted == total and compelted != 0)  else 'in progress',
        'application_state': application_state
    }

@app.route('/start', methods=['POST'])
def start():
    # set application_state_code to 1

    state = ApplicationState.query.filter_by(key='application_state_code').first()
    # set value to 1
    state.value = '1'
    # commit the changes
    db.session.commit()
    # store the excel file in static folder
    return read_data_from_excel_file(request.files['file'])




# ---------------------
# ---------------------

process_collection = []
# a function to read dat from excel file 
def read_data_from_excel_file(file_path):
    global app
    # truncate Product table
    Product.query.delete()
    # commit the changes
    db.session.commit()
    # read data from excel file 
    data = pd.read_excel(file_path)
    # iterate over each row in data
    i = 1
    for index, row in data.iterrows():
        product = Product(sku=row[0])
        # add product to database
        db.session.add(product)
        # commit the changes
        db.session.commit()
    # set application state to 2
    state = ApplicationState.query.filter_by(key='application_state_code').first()
    # set value to 2
    state.value = '2'
    # commit the changes
    db.session.commit()
    for index, row in data.iterrows():
        # take first column as sku 
        sku = str(row[0])
        # seperate_sku_process(sku)
        # seperate sku process
        process = mp.Process(target=seperate_sku_process, args=(sku,i))
        process.start()
        process_collection.append(process)
        # sleep for 1 second
        print("started process for sku " + sku + " i " + str(i))
        time.sleep(9)
        if i % 10 == 0:
            # until process_collection is not empty, pop one process and join
            while len(process_collection) > 0:
                p = process_collection.pop()
                print("joining process " + str(p))
                p.join()
        i+=1
    # join all processes
    while len(process_collection) > 0:
        p = process_collection.pop()
        print("joining process " + str(p))
        p.join()
    
    # get all the data from Product table in a dataframe 
    products = Product.query.all()
    # create a dataframe from products
    df = pd.DataFrame([product.to_dict() for product in products])
    # save datafraome to excel file , use date time in format YYYY_MM_DD_HH_MM_SS as file name
    df.to_excel("static/output/output_"  +  time.strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
    # set application state to 4
    state = ApplicationState.query.filter_by(key='application_state_code').first()
    # set value to 4
    state.value = '4'
    # commit the changes
    db.session.commit()


def seperate_sku_process(sku, i):
    from app import app, db, Product

    # search_key_1 will be sku itself 
    search_key_1 = sku
    # search_key_2 will be only numeric part of sku
    # replace all non numeric characters with empty string
    search_key_2 = ''.join(i for i in sku if i.isdigit())
    # fetch data from https://www.gsaadvantage.gov/advantage/rs/search/advantage_search?q=0:8UNV61683&db=0&searchType=0 
    url = "https://www.gsaadvantage.gov/advantage/rs/search/advantage_search?q=0:8" + sku + "&db=0&searchType=0"
    # get data from url
    # with content type json
    try:
        wait_times = [22, 42, 62, 82, 102, 122, 142, 162, 182, 202]
        wait_times_len = len(wait_times)
        wait_index = 0
        not_break = True
        while not_break: 
            response = requests.get(url, headers={
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Accept-encoding': 'gzip, deflate, br',        
            })
            if response.status_code != 200:
                # raise Exception("Error in fetching data from sku " + sku + " status code " + str(response.status_code))
                wait_time_seconds = wait_times[wait_index]
                print("Error in fetching data from sku " + sku + " status code " + str(response.status_code) + " retrying in " +  str(wait_time_seconds) + " seconds")
                # sleep for 5 seconds 
                time.sleep(wait_time_seconds)
                # increment wait_index
                if wait_index < wait_times_len - 1:
                    wait_index += 1
                continue
            not_break = False
        data = response.json()
        # iterate over solrResultList.productResults
        contractors = []
        for product in data['solrResultList']['productResults']:
            if search_key_1 == product['mfrPartNumber'] or search_key_2 == product['mfrPartNumber']:
                cnt = fetch_top_contractor_for_gsin(product['gsin'])
                # iterate and append contractors
                for c in cnt:
                    contractor = {}
                    contractor['name'] = c['vendorName']
                    contractor['price'] = c['price']
                    # check if features key list has SALE 
                    contractor['has_sale'] = 'Yes' if 'SALE' in c['features'] else 'No'
                    contractor['price'] = c['price']['unitPrice']
                
                    contractors.append(contractor)
        # sort contractors by price
        contractors = sorted(contractors, key=lambda k: k['price'])
        # also update any product with same sku 
        # iterate over each product 
        with app.test_request_context('/'):
            products = Product.query.filter_by(sku=sku).all()
            # iterate over each product
            for product in products:
                # iterate over each contractor
                for index, contractor in enumerate(contractors):
                    # update contractor name
                    setattr(product, 'contractor_' + str(index + 1), contractor['name'])
                    # update contractor price
                    setattr(product, 'price_' + str(index + 1), contractor['price'])
                    # update contractor has_sale
                    setattr(product, 'has_sale_' + str(index + 1), contractor['has_sale'])
                # set is_completed column to 1 
                setattr(product, 'is_completed', 2)
                # commit the changes
                # update the product 
                db.session.commit()
        
        print("updated product for sku " + sku + " index " + str(i))
    except Exception as e:
        # log the error 
        print("Error in fetching data from sku " + sku)
        # write error in log file
        with open("log.txt", "a") as log_file:
            log_file.write("Error in fetching data from sku " + sku + "\n")
            # error message 
            log_file.write(str(e) + "\n")
            # also stack strace 

def fetch_top_contractor_for_gsin(gsin):
    # https://www.gsaadvantage.gov/advantage/rs/catalog/product_detail?gsin=11000000949094
    url = "https://www.gsaadvantage.gov/advantage/rs/catalog/product_detail?gsin=" + gsin
    # get data from url
    # with content type json
    try:
        wait_times = [22, 42, 62, 82, 102, 122, 142, 162, 182, 202]
        wait_times_len = len(wait_times)
        wait_index = 0
        not_break = True
        while not_break:
            response = requests.get(url, headers={
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Accept-encoding': 'gzip, deflate, br',        
            })
            # if response status code is not 200
            if response.status_code != 200:
                # raise Exception("Error in fetching data from gsin " + gsin + " status code " + str(response.status_code))
                wait_time_seconds = wait_times[wait_index]
                print("Error in fetching data from gsin " + gsin + " status code " + str(response.status_code) + " retrying in " +  str(wait_time_seconds) + " seconds")
                # sleep for 5 seconds
                time.sleep(wait_time_seconds)
                # increment wait_index
                if wait_index < wait_times_len - 1:
                    wait_index += 1
                continue
            not_break = False
        data = response.json()
        # iterate over productDetailVO.products
        return data['productDetailVO']['products'][:10]
    except Exception as e:
        # log the error 
        print("Error in fetching data from gsin " + gsin)
        # write error in log file
        with open("log.txt", "a") as log_file:
            log_file.write("Error in fetching data from gsin " + gsin + "\n")
            # error message 
            log_file.write(str(e) + "\n")






if __name__ == "__main__":
    with app.app_context():
        # create all tables
        db.create_all()
        # check if MainConfig table has row with company_name key 
        # if not then add it
        if MainConfig.query.filter_by(key='company_name').count() == 0:
            # add company_name to MainConfig table
            main_config = MainConfig(key='company_name', value='Company Name')
            # add main_config to database
            db.session.add(main_config)
            # commit the changes
            db.session.commit()

        # check if RunTimeConfig has row with sleep between sku key
        # if not then add it
        if RunTimeConfig.query.filter_by(key='sleep_between_sku').count() == 0:
            # add sleep_between_sku to RunTimeConfig table
            run_time_config = RunTimeConfig(key='sleep_between_sku', value='2')
            # add run_time_config to database
            db.session.add(run_time_config)
            # commit the changes
            db.session.commit()
        # check if RunTimeConfig has row with batch_size key
        # if not then add it
        if RunTimeConfig.query.filter_by(key='batch_size').count() == 0:
            # add batch_size to RunTimeConfig table
            run_time_config = RunTimeConfig(key='batch_size', value='10')
            # add run_time_config to database
            db.session.add(run_time_config)
            # commit the changes
            db.session.commit()
        # check if RunTimeConfig has row with error_sleep_second_list 
        # if not then add it
        if RunTimeConfig.query.filter_by(key='error_sleep_second_list').count() == 0:
            # add error_sleep_second_list to RunTimeConfig table
            run_time_config = RunTimeConfig(key='error_sleep_second_list', value='22,42,62,82,102,122,142,162,182,202')
            # add run_time_config to database
            db.session.add(run_time_config)
            # commit the changes
            db.session.commit()
        # check if ApplicationState table has row with application_state_code 
        # if not then add it
        if ApplicationState.query.filter_by(key='application_state_code').count() == 0:
            # add application_state_code to ApplicationState table
            application_state = ApplicationState(key='application_state_code', value='0')
            # 0 means application is not running
            # 1 means application is processing the uploaded excel file
            # 2 means application is processing the uploaded excel file and updating the database
            # 3 means the state is paused 
            # 4 means the state is finished
            # add application_state to database
            db.session.add(application_state)
            # commit the changes
            db.session.commit()
        # check if ApplicationState table has row with sleep_status
        # if not then add it
        if ApplicationState.query.filter_by(key='sleep_status').count() == 0:
            # add sleep_status to ApplicationState table
            application_state = ApplicationState(key='sleep_status', value='0')
            # 0 means sleep is off
            # 1 means sleep is on and all application will stop
            # add application_state to database
            db.session.add(application_state)
            # commit the changes
            db.session.commit()

    app.run(debug=True)