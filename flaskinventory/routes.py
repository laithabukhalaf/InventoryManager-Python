from flask import  render_template,url_for,redirect,request
from flaskinventory import app,db
from flaskinventory.forms import addproduct,addlocation,moveproduct,editproduct,editlocation
from flaskinventory.models import Location,Product,Movement,Balance
import time,datetime



@app.route("/Overview")
@app.route("/")
def overview():
    balance = Balance.query.all()
    # return render_template('overview.html' ,balance=balance)
    locations = [x.loc_name for x in Location.query.all()]
    products = [x.prod_name for x in Product.query.all()]

    grid = [ [0]*len(locations) for i in range(len(products))]
    for entry in balance:
        product_index = products.index(entry.product)
        location_index = locations.index(entry.location)

        grid[product_index][location_index] = entry.quantity

    return render_template('overview.html' ,locations=locations,products=products,grid=grid)




@app.route("/Product", methods = ['GET','POST'])
def product():
    form = addproduct()
    eform = editproduct()
    details = Product.query.all()
    
    if eform.validate_on_submit() and request.method == 'POST':

        p_id = request.form.get("productid","")# 2-for default
        pname = request.form.get("productname","")
        details = Product.query.all()
        prod = Product.query.filter_by(prod_id = p_id).first()
        prod.prod_name = eform.editname.data
       
        Balance.query.filter_by(product=pname).update(dict(product=eform.editname.data))
        Movement.query.filter_by(pname=pname).update(dict(pname=eform.editname.data))
        
        try:
            db.session.commit()
            return redirect('/Product')
        except:
            db.session.rollback()
            return redirect('/Product')
        return render_template('product.html',title = 'Products',details=details,eform=eform)

    elif form.validate_on_submit() :
        product = Product(prod_name=form.prodname.data)
        db.session.add(product)
        try:
            db.session.commit()
            return redirect('/Product')
        except:
            db.session.rollback()
            return redirect('/Product')
    return render_template('product.html',title = 'Products',eform=eform,form = form,details=details)




@app.route("/Location", methods = ['GET', 'POST'])
def loc():
    form = addlocation()
    lform = editlocation()
    details = Location.query.all()
    
    
    if lform.validate_on_submit() and request.method == 'POST':
        p_id = request.form.get("locid","")
        locname = request.form.get("locname","")
        details = Location.query.all()
        
        loc = Location.query.filter_by(loc_id = p_id).first()
        loc.loc_name = lform.editlocname.data
        Balance.query.filter_by(location=locname).update(dict(location=lform.editlocname.data))
        Movement.query.filter_by(frm=locname).update(dict(frm=lform.editlocname.data))
        Movement.query.filter_by(to=locname).update(dict(to=lform.editlocname.data))
        try:
            db.session.commit()
          
            return redirect('/Location')
        except  :
            db.session.rollback()
            
            return redirect('/Location')
    elif form.validate_on_submit() :
        loc = Location(loc_name=form.locname.data)
        db.session.add(loc)
        try:
            db.session.commit()
            
            return redirect('/Location')
        except  :
            db.session.rollback()
            
            return redirect('/Location')
    return render_template('loc.html',title = 'Locations',lform=lform,form = form,details=details)



@app.route("/Transfers", methods = ['GET', 'POST'])
def move():
    form = moveproduct()
    details = Movement.query.all()
    pdetails = Product.query.all()
    
    #----------------------------------------------------------
    prod_choices = Product.query.with_entities(Product.prod_name,Product.prod_name).all()
    loc_choices = Location.query.with_entities(Location.loc_name,Location.loc_name).all()
    prod_list_names = []
    src_list_names,dest_list_names=[('','')],[('','')]
    prod_list_names+=prod_choices
    src_list_names+=loc_choices
    dest_list_names+=loc_choices
    #passing list_names to the form for select field
    form.mprodname.choices = prod_list_names
    form.src.choices = src_list_names
    form.destination.choices = dest_list_names
    #--------------------------------------------------------------
    #send to db
    if form.validate_on_submit() and request.method == 'POST' :

        timestamp = datetime.datetime.now()
        boolbeans = check(form.src.data,form.destination.data,form.mprodname.data,form.mprodqty.data)
        if boolbeans != False:
            mov = Movement(ts=timestamp,frm=form.src.data,to = form.destination.data,
                        pname=form.mprodname.data,pqty=form.mprodqty.data)
            db.session.add(mov)
            db.session.commit()
            
        return redirect('/Transfers')
    return render_template('move.html',title = 'Transfers',form = form,details= details)

def check(frm,to,name,qty):
    if frm == to:
        return False
        
    elif frm =='' and to != '':
        prodq = Product.query.filter_by(prod_name=name).first()
        
        bal = Balance.query.filter_by(location=to,product=name).first()
        a=str(bal)
        if(a=='None'):
            new = Balance(product=name,location=to,quantity=qty)
            db.session.add(new)
        else:
            bal.quantity += qty
        db.session.commit()
        
    elif to == '' and frm != '':
        bal = Balance.query.filter_by(location=frm,product=name).first()
        a=str(bal)
        if a=='None' or bal.quantity<qty:
            return False
        else:
            bal.quantity -= qty
        db.session.commit()
            

    else: #from='?' and to='?'
        bl = Balance.query.filter_by(location=frm,product=name).first() #check if from location is in Balance
        
        
        #quantity is enough
        bal = Balance.query.filter_by(location=to,product=name).first()
        a = str(bal)
        if a=='None':
            #if not add entry(bdeef jdeed)
            new = Balance(product=name,location=to,quantity=qty)
            db.session.add(new)
            bl = Balance.query.filter_by(location=frm,product=name).first()
            if bl.quantity<qty:
               return False
            elif bl.quantity>qty:
                bl.quantity -= qty
            
            db.session.commit()
        else:#else add to 'to' qty and minus from 'from' qty
                bl = Balance.query.filter_by(location=frm,product=name).first()

                if bl== None:#deft ana hoon 
                    return False
                elif bl.quantity<qty:
                    return False
                else:
                    bal.quantity += qty #if yes,add to to qty
                    bl.quantity -= qty
                db.session.commit()

@app.route("/delete")
def delete():
    type = request.args.get('type')#location or product
    if type == 'product':
        pid = request.args.get('p_id')
        product = Product.query.filter_by(prod_id=pid).delete()
        db.session.commit()
        
        return redirect('/Product')
  
    else:
        pid = request.args.get('p_id')
        loc = Location.query.filter_by(loc_id = pid).delete()
        db.session.commit()
        
        return redirect('/Location')
        
