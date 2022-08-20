from flask import Flask,request,render_template,redirect,url_for,Response
import pandas as pd
import os

app=Flask(__name__)
app.secret_key="SDGASGW"
app.config['UPLOAD_FOLDER']="static\Excel"

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/",methods=['GET','POST'])
def upload():
    if request.method == "POST":
        uploadExcel = request.files["uploadExcel"]
        uploadname = request.form["uploadname"] + ".csv"
        try:
            if uploadExcel.filename != "":

                filepath=os.path.join(app.config['UPLOAD_FOLDER'], uploadExcel.filename)
            
                df=pd.read_csv(filepath).dropna().drop_duplicates()
                column_name=list(df.columns.values)
                dateval=["date","Date","Year","year","DATE","YEAR"]
                for dateitem in dateval:
                    if dateitem in column_name:
                        df[dateitem]=pd.to_datetime(df[dateitem])

            
                uploadExcel.save(df.to_csv(uploadname))

        except:
            return redirect(url_for("success"))
            
            
    return render_template("upload.html")

if __name__ == '__main__':
    app.run(debug=True)