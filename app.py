from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import numpy as np 
import pandas as pd 
import requests
import multiprocessing as mp
# from app import db, Product
import time
import hashlib
import os
app = Flask(__name__)
application = app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://scraperuser:so#meScrapper123123Password@localhost:3306/scraper'
# connection to mysql datbase uri from env variab
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

    def __repr__(self):
        return '<RunTimeConfig %r>' % self.key
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
    # 0 not started 
    # 1 started
    # 2 paused 
    # 3 error 
    # 4 completed
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
            'is_completed': self.is_completed,
            'error_message': self.error_message
        }
    

@app.route('/')
def index():
    # get data from run time config table
    # get sleep_between_sku
    sleep_between_sku = RunTimeConfig.query.filter_by(key='sleep_between_sku').first()
    # get batch_size
    batch_size = RunTimeConfig.query.filter_by(key='batch_size').first()

    company_name = MainConfig.query.filter_by(key='company_name').first()
    # get error_sleep_second_list
    error_sleep_second_list = RunTimeConfig.query.filter_by(key='error_sleep_second_list').first()
    

    error_message = request.args.get('error')
    return render_template(
        'index.html', 
        sleep_between_sku=sleep_between_sku.value, 
        batch_size=batch_size.value, 
        error_sleep_second_list=error_sleep_second_list.value,
        company_name=company_name.value,
        error_message=error_message
        )

@app.route('/reset', methods=['POST'])
def reset():
    # check password
    # get password from request
    password = request.form['security_password']
    # find hash of the password to compare 
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), b'salt', 150000)
    password_hash = password_hash.hex()
    # get password_hash from MainConfig table
    main_config = MainConfig.query.filter_by(key='password_hash').first()
    # check if password is correct
    if password_hash != main_config.value:
        # with http status code 401
        return {
            'status': 'error',
            'message': 'Incorrect Password'
        }, 401

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
    for file in os.listdir("/var/www/scraper/main/static/output"):
        files.append({
            'name': file,
            'last_modified': datetime.fromtimestamp(os.path.getmtime("/var/www/scraper/main/static/output/" + file)).strftime("%Y-%m-%d %H:%M:%S"),
            # if the last modified date is less than 1 hr, then term it as new 
            'is_new': True if (datetime.now() - datetime.fromtimestamp(os.path.getmtime("/var/www/scraper/main/static/output/" + file))).total_seconds() < 300 else False
        })
    # return as json 
    # reverset the list 
    files.reverse()
    return {
        'files': files
    }

# delete all files 
@app.route('/delete-file', methods=['POST'])
def delete_files():
    # delete file from filename in request 
    filename = request.form['filename']
    # delete file from static/output
    import os
    os.remove("/var/www/scraper/main/static/output/" + filename)
    return {
        'status': 'success'
    }

@app.route('/progress')
def progress():
    # check data from Product table
    # get list of product with is_completed = 0 and is_completed != 0 
    # get count of both
    # return as json

    compelted = Product.query.filter(Product.is_completed == 4).count()
    total = Product.query.count()
    # is_completed_0 = Product.query.filter(Product.is_completed == 0).count()


    # get all rows from ApplicationState table
    application_state = ApplicationState.query.all()
    # print(application_state)
    # set key as index
    application_state = {row.key: row.value for row in application_state}
    # application_state['application_state_code'] = 1;
    # all product with is_completed != 0 and is_completed != 4
    all_product = Product.query.filter(Product.is_completed != 0).filter(Product.is_completed != 4).all()
    # last modified file from status/output 
    return {
        'completed': compelted,
        'total' : total,
        'progress': round((compelted / total) * 100, 2) if total > 0 else 0,
        'status': 'completed' if (compelted == total and compelted != 0)  else 'in progress',
        'application_state': application_state,
        'all_product': [product.to_dict() for product in all_product]
    }

@app.route('/start', methods=['POST'])
def start():
    # from app import check_process
    pid = os.getpid()
    print("pid- 1", pid)
    # check password
    # get password from request
    password = request.form['security_password']
    # find hash of the password to compare 
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), b'salt', 150000)
    password_hash = password_hash.hex()
    # get password_hash from MainConfig table
    main_config = MainConfig.query.filter_by(key='password_hash').first()
    # check if password is correct
    if password_hash != main_config.value:
        # with http status code 401
        return {
            'status': 'error',
            'message': 'Incorrect Password'
        }, 401

    # set application_state_code to 1
    state = ApplicationState.query.filter_by(key='application_state_code').first()
    # set value to 1
    state.value = '1'
    # commit the changes
    db.session.commit()
    main_config = get_main_config()
    # store the excel file in static folder
    file = request.files['file']
    data = pd.read_excel(file)
    process = mp.Process(target=read_data_from_excel_file, args=(data, main_config))
    process.start()
    process_pid = process.pid
    check_pro = mp.Process(target=check_process, args=(process_pid,))
    check_pro.start()
    # join the process
    process.join()
    # kill the process
    process.terminate()
    return {
        'status': 'success'
    }


@app.route('/resume-progress', methods=['GET'])
def resume_progress():
    # from app import check_process
    # get pid from application state table
    pid = ApplicationState.query.filter_by(key='process_id').first().value
    if pid is None:
        return "Great - pid " + str(pid)
    # check if process is running
    if check_pid(int(pid)):
        return "Process is running........................"
    # # get all the data from MainConfig table
    main_config = get_main_config()
    process = mp.Process(target=continue_process, args=(main_config,))
    process.start()
    process_pid = process.pid
    check_pro = mp.Process(target=check_process, args=(process_pid,))
    check_pro.start()
    # join the process
    process.join()
    # kill the process
    process.terminate()
    return "Great - pid " + str(pid)

@app.route('/pause', methods=['POST'])
def pause():
    # check password
    # get password from request
    password = request.form['security_password']
    # find hash of the password to compare 
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), b'salt', 150000)
    password_hash = password_hash.hex()
    # get password_hash from MainConfig table
    main_config = MainConfig.query.filter_by(key='password_hash').first()
    # check if password is correct
    if password_hash != main_config.value:
        # with http status code 401
        return {
            'status': 'error',
            'message': 'Incorrect Password'
        }, 401
    # set application_state_code to 3
    state = ApplicationState.query.filter_by(key='application_state_code').first()
    # set value to 3
    state.value = '3'
    # commit the changes
    db.session.commit()
    return {
        'status': 'success'
    }

@app.route('/resume-progress', methods=['GET'])
def resume_progress():
    # get num_try from session 
    num_try = session.get('num_try', 0)
    session['num_try'] = num_try + 1
    # store it back 
    session.modified = True
    # from app import check_process
    # get pid from application state table
    pid = ApplicationState.query.filter_by(key='process_id').first().value

    if pid is None:
        # increment num_try and store in session
        
        return "No Process ID found - application is not running - pid " + str(pid) + " num_try " + str(num_try)
    # check if process is running
    if check_pid(int(pid)) and num_try < 5:
        return "Process is running........................ " + str(pid) + " num_try " + str(num_try)
    
    # # get all the data from MainConfig table
    main_config = get_main_config()
    # set num_try to 0
    session['num_try'] = 0
    # store it back
    session.modified = True
    process = mp.Process(target=continue_process, args=(main_config,))
    process.start()
    process_pid = process.pid
    check_pro = mp.Process(target=check_process, args=(process_pid,))
    check_pro.start()
    # join the process
    process.join()
    # kill the process
    process.terminate()
    return "Great - pid " + str(pid)

# force generate excel file 
@app.route('/force-generate-excel-file', methods=['GET'])
def force_generate_excel_file():
    # type from query 
    type_q = request.args.get('type')

    if type_q == 'complete':
        products = Product.query.filter(Product.is_completed == 4).all()
    else:
        products = Product.query.filter(db.not_(Product.is_completed != 4) | (Product.is_completed == None)).all()

    # create a dataframe from products
    df = pd.DataFrame([product.to_dict() for product in products])
    # drop is_completed and error_message column
    df = df.drop(['is_completed', 'error_message'], axis=1)
    # save datafraome to excel file , use date time in format YYYY_MM_DD_HH_MM_SS as file name, without index
    df.to_excel("/var/www/scraper/main/static/output/output_" + type_q + "_" + time.strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx", index = False)
    # redirect b ack to home page
    return redirect('/')

@app.route('/store-run-time-config', methods=['POST'])
def store_run_time_config():
    # check password
    # get password from request
    password = request.form['security_password']
    # find hash of the password to compare 
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), b'salt', 150000)
    password_hash = password_hash.hex()
    # get password_hash from MainConfig table
    main_config = MainConfig.query.filter_by(key='password_hash').first()
    # check if password is correct
    if password_hash != main_config.value:
        # redirect to home page with error message
        return redirect('/?error=Incorrect Password')

    # get sleep_between_sku
    sleep_between_sku = request.form['sleep_between_sku']
    # get batch_size
    batch_size = request.form['batch_size']
    # get error_sleep_second_list
    error_sleep_second_list = request.form['error_sleep_second_list']
    # get all the data from RunTimeConfig table
    run_time_config = RunTimeConfig.query.all()
    # set key as index
    run_time_config = {row.key: row for row in run_time_config}
    # update sleep_between_sku
    run_time_config['sleep_between_sku'].value = sleep_between_sku
    # update batch_size
    run_time_config['batch_size'].value = batch_size
    # update error_sleep_second_list
    run_time_config['error_sleep_second_list'].value = error_sleep_second_list
    # commit the changes
    db.session.commit()
    return redirect('/')

@app.route('/store-main-config', methods=['POST'])
def store_main_config():
    # check password
    # get password from request
    password = request.form['security_password']
    # find hash of the password to compare 
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), b'salt', 150000)
    password_hash = password_hash.hex()
    # get password_hash from MainConfig table
    main_config = MainConfig.query.filter_by(key='password_hash').first()
    # check if password is correct
    if password_hash != main_config.value:
        # redirect to home page with error message
        return redirect('/?error=Incorrect Password')

    # get company_name
    company_name = request.form['company_name']
    # get all the data from MainConfig table
    main_config = MainConfig.query.all()
    # set key as index
    main_config = {row.key: row for row in main_config}
    # update company_name
    main_config['company_name'].value = company_name

    # if new_password is not empty
    new_password = request.form['new_password']
    if new_password != '':
        # update password_hash
        main_config['password_hash'].value = hashlib.pbkdf2_hmac('sha256', new_password.encode('utf-8'), b'salt', 150000).hex()
    # commit the changes
    db.session.commit()
    return redirect('/')


# ---------------------
# ---------------------

# a function to read dat from excel file 
def read_data_from_excel_file(data, main_config):
    from app import app, db, Product, ApplicationState
    with app.app_context():
        process_collection = []
        # get current process id 
        pid = os.getpid()
        print("pid- 2", pid)
        # check_process = mp.Process(target=check_process, args=(pid,))
        # check_process.start()
        # store process_id in ApplicationState table
        state = ApplicationState.query.filter_by(key='process_id').first()
        if state is None:
            # create a new row in ApplicationState table
            state = ApplicationState(key='process_id', value=str(pid))
            # add state to database
            db.session.add(state)
            # commit the changes
            db.session.commit()
        else:
            # update process_id
            state.value = str(pid)
            # commit the changes
            db.session.commit()
        # truncate Product table
        Product.query.delete()
        # commit the changes
        db.session.commit()
        # read data from excel file 
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
            # check if application state is 3
            pause_loop = True
            while pause_loop:
                # get application state , latest, no cashing 
                application_state = ApplicationState.query.filter_by(key='application_state_code').first()
                db.session.refresh(application_state)
                # if application state is 3 then sleep for 5 seconds
                print("status",application_state.value, application_state.value == '3', application_state.value == 3)
                if application_state.value == '3':
                    print("Application is paused")
                    # sleep for 5 seconds
                    time.sleep(5)
                    continue
                elif application_state.value == '0':
                    # stop the process
                    print("Application is stopped")
                    exit()
                else:
                    print("Application is running")
                    pause_loop = False


            # take first column as sku 
            sku = str(row[0])
            # seperate_sku_process(sku)
            # seperate sku process
            process = mp.Process(target=seperate_sku_process, args=(sku,i,main_config['company_name'], get_runtime_config))
            print(509)
            process.start()
            process_collection.append(process)
            # sleep for 1 second
            print("started process for sku " + sku + " i " + str(i))

            run_time_config = get_runtime_config()
            time.sleep(int(run_time_config['sleep_between_sku']))
            if i % int(run_time_config['batch_size']) == 0:
                # until process_collection is not empty, pop one process and join
                while len(process_collection) > 0:
                    p = process_collection.pop()
                    print("joining process " + str(p))
                    p.join()
                    p.terminate()
            i+=1
        
        while len(process_collection) > 0:
            p = process_collection.pop()
            print("joining process " + str(p))
            p.join()
            p.terminate()
        products = Product.query.filter((Product.is_completed != 4) | (Product.is_completed == None)).all()
        # iterate over each product
        i = 0
        for product in products:
            if product.is_completed == 4:
                print("Process already completed for product - " + product.sku)
                continue
            print("Retrying for sku " + product.sku)
            # check if application state is 3
            pause_loop = True
            while pause_loop:
                # get application state , latest, no cashing 
                application_state = ApplicationState.query.filter_by(key='application_state_code').first()
                db.session.refresh(application_state)
                # if application state is 3 then sleep for 5 seconds
                print("status",application_state.value, application_state.value == '3', application_state.value == 3)
                if application_state.value == '3':
                    print("Application is paused")
                    # sleep for 5 seconds
                    time.sleep(5)
                    continue
                elif application_state.value == '0':
                    # stop the process
                    print("Application is stopped")
                    return {
                        'status': 'success'
                    }
                else:
                    print("Application is running")
                    pause_loop = False


            # take first column as sku 
            sku = str(product.sku)
            # seperate_sku_process(sku)
            # seperate sku process
            process = mp.Process(target=seperate_sku_process, args=(sku,i,main_config['company_name'], get_runtime_config))
            process.start()
            process_collection.append(process)
            # sleep for 1 second
            print("started process for sku " + sku + " i " + str(i))

            run_time_config = get_runtime_config()
            time.sleep(int(run_time_config['sleep_between_sku']))
            if i % 1 == 0:
                # until process_collection is not empty, pop one process and join
                while len(process_collection) > 0:
                    p = process_collection.pop()
                    print("joining process " + str(p))
                    p.join()
                    p.terminate()
            i+=1
        # join all processes
        while len(process_collection) > 0:
            p = process_collection.pop()
            print("joining process " + str(p))
            p.join()
            p.terminate()
        
        # get all the data from Product table in a dataframe 
        products = Product.query.all()
        # create a dataframe from products
        df = pd.DataFrame([product.to_dict() for product in products])
        # drop is_completed and error_message column
        df = df.drop(['is_completed', 'error_message'], axis=1)
        # save datafraome to excel file , use date time in format YYYY_MM_DD_HH_MM_SS as file name
        df.to_excel("/var/www/scraper/main/static/output/output_"  +  time.strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
        # set application state to 4
        state = ApplicationState.query.filter_by(key='application_state_code').first()
        # set value to 4
        state.value = '4'
        # commit the changes
        db.session.commit()

# a function to read dat from excel file 
def continue_process(main_config):
    print("Continuing process")
    from app import app, db, Product, ApplicationState
    with app.app_context():
        process_collection = []
        # get current process id
        pid = os.getpid()
        # store process_id in ApplicationState table
        state = ApplicationState.query.filter_by(key='process_id').first()
        if state is None:
            # create a new row in ApplicationState table
            state = ApplicationState(key='process_id', value=str(pid))
            # add state to database
            db.session.add(state)
            # commit the changes
            db.session.commit()
        else:
            # update process_id
            state.value = str(pid)
            # commit the changes
            db.session.commit()
        # set application state to 2
        state = ApplicationState.query.filter_by(key='application_state_code').first()
        # set value to 2
        state.value = '2'
        # commit the changes
        db.session.commit()

        data = Product.query.filter((Product.is_completed != 4) | (Product.is_completed == None)).all()
        print(len(data))
        i = 0
        for row in data:
            # check if application state is 3
            pause_loop = True
            while pause_loop:
                # get application state , latest, no cashing 
                application_state = ApplicationState.query.filter_by(key='application_state_code').first()
                db.session.refresh(application_state)
                # if application state is 3 then sleep for 5 seconds
                print("status",application_state.value, application_state.value == '3', application_state.value == 3)
                if application_state.value == '3':
                    print("Application is paused")
                    # sleep for 5 seconds
                    time.sleep(5)
                    continue
                elif application_state.value == '0':
                    # stop the process
                    print("Application is stopped")
                    return {
                        'status': 'success'
                    }
                else:
                    print("Application is running")
                    pause_loop = False


            # take first column as sku 
            sku = str(row.sku)
            # seperate_sku_process(sku)
            # seperate sku process
            process = mp.Process(target=seperate_sku_process, args=(sku,i,main_config['company_name'], get_runtime_config))
            process.start()
            process_collection.append(process)
            # sleep for 1 second
            print("started process for sku " + sku + " i " + str(i))

            run_time_config = get_runtime_config()
            time.sleep(int(run_time_config['sleep_between_sku']))
            if i % int(run_time_config['batch_size']) == 0:
                # until process_collection is not empty, pop one process and join
                while len(process_collection) > 0:
                    p = process_collection.pop()
                    print("joining process " + str(p))
                    p.join()
                    p.terminate()
            i+=1
        
        while len(process_collection) > 0:
            p = process_collection.pop()
            print("joining process " + str(p))
            p.join()
            p.terminate()
        products = Product.query.filter((Product.is_completed != 4) | (Product.is_completed == None)).all()
        # iterate over each product
        i = 0
        for product in products:
            if product.is_completed == 4:
                print("Process already completed for product - " + product.sku)
                continue
            print("Retrying for sku " + product.sku)
            # check if application state is 3
            pause_loop = True
            while pause_loop:
                # get application state , latest, no cashing 
                application_state = ApplicationState.query.filter_by(key='application_state_code').first()
                db.session.refresh(application_state)
                # if application state is 3 then sleep for 5 seconds
                print("status",application_state.value, application_state.value == '3', application_state.value == 3)
                if application_state.value == '3':
                    print("Application is paused")
                    # sleep for 5 seconds
                    time.sleep(5)
                    continue
                elif application_state.value == '0':
                    # stop the process
                    print("Application is stopped")
                    return {
                        'status': 'success'
                    }
                else:
                    print("Application is running")
                    pause_loop = False


            # take first column as sku 
            sku = str(product.sku)
            # seperate_sku_process(sku)
            # seperate sku process
            process = mp.Process(target=seperate_sku_process, args=(sku,i,main_config['company_name'], get_runtime_config))
            process.start()
            process_collection.append(process)
            # sleep for 1 second
            print("started process for sku " + sku + " i " + str(i))

            run_time_config = get_runtime_config()
            time.sleep(int(run_time_config['sleep_between_sku']))
            if i % 1 == 0:
                # until process_collection is not empty, pop one process and join
                while len(process_collection) > 0:
                    p = process_collection.pop()
                    print("joining process " + str(p))
                    p.join()
                    p.terminate()
            i+=1
        # join all processes
        while len(process_collection) > 0:
            p = process_collection.pop()
            print("joining process " + str(p))
            p.join()
            p.terminate()
        
        # get all the data from Product table in a dataframe 
        products = Product.query.all()
        # create a dataframe from products
        df = pd.DataFrame([product.to_dict() for product in products])
        # drop is_completed and error_message column
        df = df.drop(['is_completed', 'error_message'], axis=1)
        # save datafraome to excel file , use date time in format YYYY_MM_DD_HH_MM_SS as file name
        df.to_excel("/var/www/scraper/main/static/output/output_"  +  time.strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
        # set application state to 4
        state = ApplicationState.query.filter_by(key='application_state_code').first()
        # set value to 4
        state.value = '4'
        # commit the changes
        db.session.commit()


def seperate_sku_process(sku, i, company_name, get_runtime_config):
    from app import app, db, Product, RunTimeConfig
    with app.app_context():
        run_time_configs = RunTimeConfig.query.filter_by(key='error_sleep_second_list').first()
        # get error_sleep_second_list
        error_sleep_second_list = run_time_configs.value.split(',')
        # strip and convert to int
        error_sleep_second_list = [int(i.strip()) for i in error_sleep_second_list]
        # update product for sku status to 1 
        # get product from database
        product = Product.query.filter_by(sku=sku).first()
        # set is_completed column to 1
        setattr(product, 'is_completed', 1)
        # commit the changes
        db.session.commit()
        # runtime_config = {row.key: row.value for row in RunTimeConfig.query.all()}
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
        wait_times = error_sleep_second_list
        print("wait_times", wait_times)
        # strip and convert to int 
        # wait_times = [int(i.strip()) for i in wait_times]
        wait_times_len = len(wait_times)
        wait_index = 0
        not_break = True
        while not_break: 
            with app.app_context():
                # update product for sku status to 1 
                # get product from database
                product = Product.query.filter_by(sku=sku).first()
                # set error_message column to empty string
                setattr(product, 'error_message', 'Fetching...')
                # set is_completed column to 1
                setattr(product, 'is_completed', 1)
                # commit the changes
                db.session.commit()
            response = requests.get(url, headers={
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Accept-encoding': 'gzip, deflate, br',        
            })
            if response.status_code != 200:
                # raise Exception("Error in fetching data from sku " + sku + " status code " + str(response.status_code))
                wait_time_seconds = wait_times[wait_index]
                print("Error in fetching data from sku " + sku + " status code " + str(response.status_code) + " retrying in " +  str(wait_time_seconds) + " seconds")
                with app.app_context():
                    # update product for sku status to 1 
                    # get product from database
                    product = Product.query.filter_by(sku=sku).first()
                    # set error_message column to error message
                    setattr(product, 'error_message', "Error in fetching data from sku " + sku + " status code " + str(response.status_code) + " retrying in " +  str(wait_time_seconds) + " seconds")
                    # set is_completed column to 2
                    setattr(product, 'is_completed', 2)
                    # commit the changes
                    db.session.commit()
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
        company_value = None
        for product in data['solrResultList']['productResults']:
            if search_key_1 == product['mfrPartNumber'] or search_key_2 == product['mfrPartNumber']:
                res = fetch_top_contractor_for_gsin(product['gsin'], sku, company_name, get_runtime_config)
                cnt = res['contractors']
                if company_value == None or (res['company_value'] and company_value > res['company_value']):
                    company_value = res['company_value']
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
                setattr(product, 'is_completed', 4)
                # company price 
                setattr(product, 'company_price', company_value)
                # commit the changes
                # update the product 
                db.session.commit()
        
        print("updated product for sku " + sku + " index " + str(i))
    except Exception as e:
        # log the error 
        print("Error in fetching data from sku " + sku)
        # write error in log file
        with open("/var/www/scraper/main/log.txt", "a") as log_file:
            # line number 
            log_file.write("Error in fetching data from sku " + sku + "\n")
            # error message 
            log_file.write(str(e) + "\n")
        exit()
        return False

def fetch_top_contractor_for_gsin(gsin, sku, company_name, get_runtime_config):
    # https://www.gsaadvantage.gov/advantage/rs/catalog/product_detail?gsin=11000000949094
    url = "https://www.gsaadvantage.gov/advantage/rs/catalog/product_detail?gsin=" + gsin
    # get data from url
    # with content type json
    
    try:
        with app.app_context():
            runtime_config = {row.key: row.value for row in RunTimeConfig.query.all()}
        wait_times = runtime_config['error_sleep_second_list'].split(',')
        # wait_times = [22, 33, 44, 55, 66, 77, 88, 99, 110, 121];
        # strip and convert to int 
        wait_times = [int(i.strip()) for i in wait_times]
        wait_times_len = len(wait_times)
        wait_index = 0
        not_break = True
        while not_break:
            with app.app_context():
                # update product for sku status to 1 
                # get product from database
                product = Product.query.filter_by(sku=sku).first()
                # set error_message column to empty string
                setattr(product, 'error_message', 'Fetching...')
                # set is_completed column to 1
                setattr(product, 'is_completed', 1)
                # commit the changes
                db.session.commit()
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
                with app.app_context():
                    # update product for sku status to 1 
                    # get product from database
                    product = Product.query.filter_by(sku=sku).first()
                    # set error_message column to error message
                    setattr(product, 'error_message', "Error in fetching data from gsin " + gsin + " status code " + str(response.status_code) + " retrying in " +  str(wait_time_seconds) + " seconds")
                    # set is_completed column to 2
                    setattr(product, 'is_completed', 2)
                    # commit the changes
                    db.session.commit()
                # sleep for 5 seconds
                time.sleep(wait_time_seconds)
                # increment wait_index
                if wait_index < wait_times_len - 1:
                    wait_index += 1
                continue
            not_break = False
        data = response.json()
        if 'responseType' in data and data['responseType'] == 'ERROR':
            return {
                'company_value' : None,
                'contractors' : []
            }

        # iterate over productDetailVO.products
        products = data['productDetailVO']['products']
        min_value = None
        for product in products:
            # compare company name, case insensitive 
            # print("\"", company_name.lower(), "\"", "\"", product['vendorName'].lower(), "\"")
            if company_name.lower() == product['vendorName'].lower():
                # print("min value updated to" )
                min_value = product['price']['unitPrice']
        return {
            'company_value' : min_value,
            'contractors' : products[:10]
        }
    except Exception as e:
        # log the error 
        print("Error in fetching data from gsin " + gsin)
        # write error in log file
        with open("/var/www/scraper/main/log.txt", "a") as log_file:
            log_file.write("Error in fetching data from gsin " + gsin + "\n")
            # error message 
            log_file.write(str(e) + "\n")
        return {
            'company_value' : None,
            'contractors' : []
        }

def get_runtime_config():
    #from app import app, db, RunTimeConfig
    #with app.app_context():
        # get all the data from RunTimeConfig table
        run_time_config = RunTimeConfig.query.all()
        # set key as index
        run_time_config = {row.key: row.value for row in run_time_config}
        return run_time_config

def get_main_config():
    # get all the data from MainConfig table
    main_config = MainConfig.query.all()
    # set key as index
    main_config = {row.key: row.value for row in main_config}
    return main_config

def check_pid(pid):
    import platform
    if platform.system() == 'Windows':
        # windows
        import ctypes
        kernel32 = ctypes.windll.kernel32
        SYNCHRONIZE = 0x100000
        process = kernel32.OpenProcess(SYNCHRONIZE, 0, pid)
        if process != 0:
            kernel32.CloseHandle(process)
            return True
        else:
            return False
    else:
        # linux
        import os
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True
            
def check_process(pid):
    print("----------------- ---- check_process called for pid " + str(pid))
    from app import app, db, MainConfig, ApplicationState
    with app.app_context():
        while True:
            # check if pid is running
            if check_pid(int(pid)):
                # sleep for 5 seconds
                print("pid is running")
                time.sleep(5)
                continue
            else:
                print("---------------- pid is not running restarting for pid " + str(pid))

                # check if Product table has any row with is_completed != 4
                try:
                    application_state = ApplicationState.query.filter_by(key='application_state_code').first()
                    db.session.refresh(application_state)
                    if application_state.value == '0' or application_state.value == '4':
                        # stop the process
                        print("Application is stopped")
                        break
                except Exception as e:
                    print("Error in fetching data from ApplicationState table")
                    # retrying in 10 seconds 
                    time.sleep(240)
                    continue

                try:
                    products = Product.query.filter(Product.is_completed != 4).count()
                except Exception as e:
                    print("Error in fetching data from Product table")
                    time.sleep(240)
                    continue
                if products == 0:
                    break
                else: 
                    main_config = get_main_config()
                    process = mp.Process(target=continue_process, args=(main_config,))
                    process.start()

                    check_prc = mp.Process(target=check_process, args=(process.pid,))
                    check_prc.start()
                    # join the process
                    process.join()
                    # kill the process
                    process.terminate()
                    return "Great - pid " + str(pid)
            
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
        # check if MainConfig table has row with password_hash 
        # if not then add it
        if MainConfig.query.filter_by(key='password_hash').count() == 0:
            # add password_hash to MainConfig table
            hsh = hashlib.pbkdf2_hmac('sha256', "pass@324".encode('utf-8'), b'salt', 150000)
            hsh = hsh.hex()
            main_config = MainConfig(key='password_hash', value=hsh)
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

