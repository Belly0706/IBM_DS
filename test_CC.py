# 1. import flask
from flask import Flask, render_template, request, jsonify, abort
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import json 


# 2. create Flask application
app = Flask(__name__)


"""
data={"one":[1, 3, 3, 5, 5, 1, 3, 5, 5],"two":[0.33, 1, 1, 1.67, 1.67, 0.33, 0.6, 0.3, 0.6],"three":[0.33, 1, 1, 0.71, 0.71, 0.43, 0.43, 0.14, 0.43 ], 
"four":[0.2, 0.6, 1.4, 1, 1.4, 0.14, 0.43, 0.43,0.43], "five":[0.2, 0.6, 1.4, 0.71, 1, 0.33, 0.71, 0.43, 0.43], "six":[1, 3, 2.33, 7, 3, 1, 0.71, 0.6, 1], 
"seven":[0.33, 1.67, 2.33, 2.33, 1.4, 1.4, 1, 0.6, 0.6], "eight":[0.2, 3.33, 7, 2.33, 2.33, 1.67, 1.67, 1, 0.6], "nine":[0.2, 1.67, 2.33, 2.33, 2.33, 1, 1.67, 1.67, 1]}
df=pd.DataFrame(data,index=[0,1,2,3,4,5,6,7,8])
print(df)

"""

# 3. define routes and funtions

@app.route('/max_vector', methods = ["GET","POST"] )

def max_vector():


    if request.method == "POST":
       

        a11 = float(request.form.get('a11'))
        a12 = float(request.form.get('a12'))
        a13 = float(request.form.get('a13'))
        a14 = float(request.form.get('a14'))

        a21 = float(request.form.get('a21'))
        a22 = float(request.form.get('a22'))
        a23 = float(request.form.get('a23'))
        a24 = float(request.form.get('a24'))

        a31 = float(request.form.get('a31'))
        a32 = float(request.form.get('a32'))
        a33 = float(request.form.get('a33'))
        a34 = float(request.form.get('a34'))

        a41 = float(request.form.get('a41'))
        a42 = float(request.form.get('a42'))
        a43 = float(request.form.get('a43'))
        a44 = float(request.form.get('a44'))

      


   
          

        data={"one":[a11, a21, a31, a41],"two":[a12, a22, a32, a42],"three":[a13, a23, a33, a43],"four":[a14, a24, a34, a44]}
        df = pd.DataFrame(data, index=["A","B","C","D"])

        df.loc['Col_sum'] = df.apply(lambda x: x.sum())

        col_sum = df.loc['Col_sum']

        df1 = df.div(col_sum, axis = 1)

        df1 = df1.drop("Col_sum", axis = 0)

        df1["Avg_vector"] = df1.apply(lambda x: x.mean(), axis = 1)
        
        avg_vector = df1['Avg_vector']

        df = df.drop("Col_sum", axis = 0)

        arr = []

        for i in range(df.shape[1]):

            x = np.dot(avg_vector, df.iloc[i])

            arr.append(x)
            
        arr_df = pd.DataFrame(arr)

        arr_df = arr_df.reset_index(drop = True)

        avg_vector = avg_vector.reset_index(drop = True)

        df2 = pd.concat([arr_df, avg_vector], axis = 1)

        df2["max_vector"] = df2[0]/df2['Avg_vector']
        #print(df2)
        df2 = df2.rename(index = {0:"one",1:"two",2: "three", 3:"four"})
        
        max_vector = df2['max_vector'] 

        ci = (max_vector.mean()-4)/3

        cr = ci/0.89
    
        max_vector = df2['max_vector'].to_json()
        
        #if cr < 0.1 :
        return jsonify(max_vector) 
        #else: 
            
            #return "请重新打分" 

'''              

@app.errorhandler(500)
def page_not_found(e):
    print(e)
    return "请将表格补充完整"
'''
            
                   


# 4. app.run to establish the server
if __name__ == '__main__':
    app.run(host = '10.178.205.30', port =5002)

