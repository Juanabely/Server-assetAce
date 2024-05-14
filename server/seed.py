# from models import admin, assets, requests, employee




                  ### REGISTRATION:
### Managers
{
    "username":"Paul",
    "password":"x0p1",
    "email":"Paul@gmail.com",
    "status":"manager"
    
}

{
    "username":"Tim",
    "password":"82Hello",
    "email":"Tim@gmail.com",
    "status":"manager"
}

{
    "username":"my_name",
    "password":"pass123",
    "email":"my_name@gmail.com",
    "status":"manager"
}


### Employees
{
    "username":"emp1",
    "password":"pass123",
    "email":"emp1@gmail.com",
    "status":"employee"
}


{
    "username":"emp2",
    "password":"pass123",
    "email":"emp2@gmail.com",
    "status":"employee"
}



{
    "username":"emp3",
    "password":"pass123",
    "email":"emp3@gmail.com",
    "status":"employee"
}


                 ### LOGIN:

### Mangers:

{
    "username":"Paul",
    "password":"x0p1",
    "status":"manager"
    
}

{
    "username":"Tim",
    "password":"82Hello",
    "status":"manager"
}

{
    "username":"my_name",
    "password":"pass123",
    "status":"manager"
}


### Employees:

{
    "username":"emp1",
    "password":"pass123",
    "status":"employee"
}
{
    "username":"emp2",
    "password":"pass123",
    
    "status":"employee"

}

{
    "username":"emp3",
    "password":"pass123",
    
    "status":"employee"
}


# Employee.query.filter_by(username = 'emp1').delete()

### Admins


# Register:

{
    "username":"Admin",
    "email":"admin@gmail.com",
    "password":"pass123",
    "authcode":"xtop19",
    "status":"admin"

} 


### Admin Login:


{
    "username":"Admin",
    "password":"pass123",
    "authcode":"xtop19",
    "status":"admin"

} 
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MTU2MTM2Mjl9.RIvQA-7T6mT9pmBRzvlZTUNuEuub0iTbqlt_aL7h0lo


# approving format
{
    "username":"Tim",
    "status":"manager"
}



### People to approve:
# Managers:

{
    "username":"Pete",
    "password":"x0p1",
    "email":"Pete@gmail.com",
    "status":"manager"
    
}


{
    "username":"Boby",
    "password":"x0p1",
    "email":"boby@gmail.com",
    "status":"manager"
    
}


{
    "username":"Alex",
    "password":"x0p1",
    "email":"alex@gmail.com",
    "status":"manager"
    
}


{
    "username":"Michael",
    "password":"x0p1",
    "email":"michael@gmail.com",
    "status":"manager"
    
}


# ------------ Employees----------#

{
    "username":"Bravo",
    "password":"x0p1",
    "email":"bravo@gmail.com",
    "status":"employee"
    
}

{
    "username":"Michael",
    "password":"x0p1",
    "email":"michael@gmail.com",
    "status":"employee"
    
}

{
    "username":"Michel",
    "password":"x0p1",
    "email":"michel@gmail.com",
    "status":"employee"
    
}





#### POST Assets: This what a manager would do

{
    "name":"Sports Car",
    "category":"logistics",
    "condition":"perfect condition",
    "image-url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSSz3csOr5P-Y68A9E970tlYaMzPuMhpeGXoo7yyu1EaQ&s"
}

{
    "name":"Table",
    "category":"furinture",
    "condition":"Okay",
    "image-url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFTGCEK7VayPL3RGE45FO8qMopq04k7FM-Mbgubzv-Ow&s"
}


{
    "name":"Pick Up",
    "category":"Event management",
    "condition":"Good",
    "image-url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQY38IixUhUxgJg_eIAVmeYTTu3mejx--v7SVlPNflsxQ&s"
}

{
    "name":"Oven",
    "category":"Catering",
    "condition":"Good",
    "image-url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTeEdww9sgWBSmlNH2B_htl95-a67EVJ5Cxkk1bDtaBrA&s"
}

{
    "name":"Oven",
    "category":"catering",
    "condition":"Good",
    "image-url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSSz3csOr5P-Y68A9E970tlYaMzPuMhpeGXoo7yyu1EaQ&s",
    "stock":10
}




# _________________Requests____________________

{
    "asset-id":2,
    "employee-id":1,
    "reason":"The table for coffee break broke",
    "quantity":1,
    "urgency":"urgent"

}


{
    "asset-id":1,
    "employee-id":2,
    "reason":"The CEO needs an sports car, #scoring the bonga points already",
    "quantity":1,
    "urgency":"supper uregent"

}


{
    "asset-id":1,
    "employee-id":3,
    "reason":"The CEO needs an sports car, #scoring the bonga points already",
    "quantity":1,
    "urgency":"supper uregent"

}



{
    "asset-id":3,
    "employee-id":3,
    "reason":"There is an innovation expo this weekend, the tents need to be set up and we really need a pick up to do so",
    "quantity":1,
    "urgency":"very uregent"

}
