var express = require('express');
var session = require('express-session');
var app = express();
const bodyParser = require('body-parser');

// required module to make calls to a REST API
const axios = require('axios');

app.use(session({
    secret: 'secret-key', // Change this to a strong, random key in production
    resave: true,
    saveUninitialized: true
}));

app.use(bodyParser.urlencoded({
    extended: true
}));

// set the view engine to ejs
app.set('view engine', 'ejs');

// Middleware to check if the user is authenticated
function isAuthenticated(req, res, next) {
    if (req.session && req.session.username) {
        return next();
    } else {
        res.redirect('/');
    }
}

// use res.render to load up an ejs view file

// New route for rendering the login page
app.get('/', function (req, res) {
  res.render("pages/index.ejs", {});
});

// Add a login route
app.post('/', function (req, res) {
  const username = req.body.username;
  const password = req.body.password;

  // For demonstration purposes, hardcoded credentials
  if (username === 'user' && password === 'password') {
      req.session.username = username; // Store the username in the session
      res.redirect('/dashboard');
  } else {
    return res.redirect('/?errorMessage=Invalid%20username%20or%20password');

}
});

app.get('/dashboard', isAuthenticated, function (req, res) {
res.render("pages/dashboard.ejs", {});
});

// Logout route
app.get('/logout', function (req, res) {
    req.session.destroy(function (err) {
        if (err) {
            console.log(err);
        } else {
            res.redirect('/');
        }
    });
});

// ... (rest of your routes)

app.get('/view', isAuthenticated, function (req, res) {
    res.render("pages/view.ejs", {});
});

app.get('/add', isAuthenticated, function (req, res) {
    res.render("pages/add.ejs", {});
});

app.get('/modify', isAuthenticated, function (req, res) {
    res.render("pages/modify.ejs", {});
});

app.get('/delete', isAuthenticated, function (req, res) {
    res.render("pages/delete.ejs", {});
});

app.get('/results', isAuthenticated, function (req, res) {
    res.render("pages/results.ejs", {});
});
// obtained from axios docs
app.post('/floor/add', isAuthenticated, function (req, res) {
    var level = req.body.level;
    var name = req.body.name;
    axios.post('http://127.0.0.1:5000/api/floor', {
        level: level,
        name: name
    })
        .then(function (response) {
            console.log(response);
            res.render('pages/results.ejs', {resultsData : response.data}); // render resonse as resultsData object 
        })
        .catch(function (error) {
            console.log(error);
        });
});
// obtained from axios docs
app.post('/room/add', isAuthenticated, function (req, res) {
    var capacity = req.body.capacity;
    var number = req.body.number;
    var floor = req.body.floor;
    axios.post('http://127.0.0.1:5000/api/room', {
        capacity: capacity,
        number: number,
        floor: floor
    })
        .then(function (response) {
            console.log(response);
            res.render('pages/results.ejs', {resultsData : response.data}); // render resonse as resultsData object 
        })
        .catch(function (error) {
            console.log(error);
        });
});
// obtained from axios docs
app.post('/resident/add', isAuthenticated, function (req, res) {
    var firstName = req.body.fname;
    var lastName = req.body.lname;
    var roomNum = req.body.room;
    var age = req.body.age;
    axios.post('http://127.0.0.1:5000/api/resident', {
        f_name: firstName,
        l_name: lastName,
        age: age,
        room: roomNum
    })
        .then(function (response) {
            console.log(response);
            res.render('pages/results.ejs', {resultsData : response.data}); // render resonse as resultsData object 
        })
        .catch(function (error) {
            console.log(error);
        });
});
// obtained from axios docs
app.get('/floor/view', isAuthenticated, function (req, res) {
    var level = req.query.level;
    // axios get requires the use of parameters as headers
    axios.get(`http://127.0.0.1:5000/api/floor/view?level=${level}`, {
        params: { level: level }
    })
    .then(function (response) {
        console.log(response);
        res.render('pages/results.ejs', {resultsData : response.data}); // render resonse as resultsData object 
    })
    .catch(function (error) {
        console.log(error);
    });
});

app.get('/room/view', isAuthenticated, function (req, res) {
    var room = req.query.number;

    axios.get(`http://127.0.0.1:5000/api/room/view?room=${room}`, {
        params: { room: room }
    })
    .then(function (response) {
        console.log(response);
        res.render('pages/results.ejs', {resultsData : response.data}); // render resonse as resultsData object 
    })
    .catch(function (error) {
        console.log(error);
    });
});

app.get('/resident/view', isAuthenticated, function (req, res) {
    var fName = req.query.fname;
    var lName = req.query.lname;
    axios.get(`http://127.0.0.1:5000/api/resident/view`, {
        params: { 
            f_name: fName,
            l_name: lName
         }
    })
    .then(function (response) {
        console.log(response);
        res.render('pages/results.ejs', {resultsData : response.data}); // render resonse as resultsData object 
    })
    .catch(function (error) {
        console.log(error);
    });
});

// obtained from axios docs
// post route used since html does not allow put method directly 
app.post('/floor/delete', isAuthenticated, function (req, res) {
    var level = req.body.level;
    // axios delete requires parameters 
    axios.delete(`http://127.0.0.1:5000/api/floor`, {
        params: { level: level }
    })
    .then(function (response) {
        console.log(response);
        res.render('pages/results.ejs', {resultsData : response.data}); // render resonse as resultsData object 
    })
    .catch(function (error) {
        console.log(error);
    });
});

app.post('/room/delete', isAuthenticated, function (req, res) {
    var number = req.body.number;

    // pass data as parameters 
    axios.delete(`http://127.0.0.1:5000/api/room`, {
        params: { 
            number: number,
        }
    })
    
    .then(function (response) {
        console.log(response);
        res.render('pages/results.ejs', {resultsData : response.data}); // render resonse as resultsData object 
    })
   
    .catch(function (error) {
        console.log(error);
    });
});
// obtained from axios docs
app.post('/resident/delete', isAuthenticated, function (req, res) {
    var firstName = req.body.fname;
    var lastName = req.body.lname;
    var age = req.body.age;
    axios.delete(`http://127.0.0.1:5000/api/resident`, {
        params: { 
            f_name: firstName,
            l_name : lastName,
            age : age
        }
    })
    .then(function (response) {
        console.log(response);
        res.render('pages/results.ejs', {resultsData : response.data}); // render resonse as resultsData object 
    })
    .catch(function (error) {
        console.log(error);
    });
});
// Update floor route
// obtained from axios docs
// post route used since html does not allow put method directly 
app.post('/floor/modify', isAuthenticated, function (req, res) {
    var level = req.body.level;
    var name = req.body.name;

    axios.put(`http://127.0.0.1:5000/api/floor`, {
        name: name,
        level: level
    })
    .then(function (response) {
        console.log(response);
        res.render('pages/results.ejs', {resultsData : response.data}); // render resonse as resultsData object 
    })
    .catch(function (error) {
        console.log(error);
    });
});

// Update room route
app.post('/room/modify', isAuthenticated, function (req, res) {
    var capacity = req.body.capacity;
    var number = req.body.number;
    var floor = req.body.floor;

    axios.put(`http://127.0.0.1:5000/api/room`, {
        capacity: capacity,
        number: number,
        floor: floor
    })
    .then(function (response) {
        console.log(response);
        res.render('pages/results.ejs', {resultsData : response.data}); // render resonse as resultsData object 
    })
    .catch(function (error) {
        console.log(error);
    });
});

// Update resident route
app.post('/resident/modify', isAuthenticated, function (req, res) {
    var firstName = req.body.fname;
    var lastName = req.body.lname;
    var roomNum = req.body.room;
    var age = req.body.age;

    axios.put(`http://127.0.0.1:5000/api/resident`, {
        f_name: firstName,
        l_name: lastName,
        age: age,
        room: roomNum
    })
    .then(function (response) {
        console.log(response);
        res.render('pages/results.ejs', {resultsData : response.data}); // render resonse as resultsData object 
    })
    .catch(function (error) {
        console.log(error);
    });
});


app.listen(8080);
console.log('8080 is the magic port');
