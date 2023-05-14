import numpy as np 
import pandas as pd 
import requests
import multiprocessing as mp
# from app import db, Product
import time

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
    i = 0
    for index, row in data.iterrows():
        product = Product(sku=row[0])
        # add product to database
        db.session.add(product)
        # commit the changes
        db.session.commit()
        # take first column as sku 
        sku = row[0]
        # seperate_sku_process(sku)
        # seperate sku process
        process = mp.Process(target=seperate_sku_process, args=(sku,i))
        process.start()
        process_collection.append(process)
        # sleep for 1 second
        print("started process for sku " + sku + " i " + str(i))
        time.sleep(4)
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
        response = requests.get(url, headers={
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Accept-encoding': 'gzip, deflate, br',        
        })
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
        # update product table
        # iterate over contractors, and index 
        # with app.test_request_context('/'):
        #     product = Product.query.filter_by(sku=sku).first()
        #     # iterate over each contractor
        #     for index, contractor in enumerate(contractors):
        #         # update contractor name
        #         setattr(product, 'contractor_' + str(index + 1), contractor['name'])
        #         # update contractor price
        #         setattr(product, 'price_' + str(index + 1), contractor['price'])
        #         # update contractor has_sale
        #         setattr(product, 'has_sale_' + str(index + 1), contractor['has_sale'])
        #     # set is_completed column to 1 
        #     setattr(product, 'is_completed', 2)
        #     # commit the changes
        #     # update the product 
        #     db.session.commit()

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
            response = requests.get(url, headers={
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Accept-encoding': 'gzip, deflate, br',        
            })
            # if response status code is not 200
            if response.status_code != 200:
                raise Exception("Error in fetching data from gsin " + gsin + " status code " + str(response.status_code))
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



# if __name__ == "__main__":
    # read data from excel file 
    # data = read_data_from_excel_file("sku.xlsx")
    # # print data 
    # print(data)


def run():
    # read data from excel file 
    data = read_data_from_excel_file("sku.xlsx")
    # # print data 
    print(data)
    # pass


