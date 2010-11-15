var month_names = ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'];
var email_regexp = /^[a-zA-z0-9\.]+@[a-zA-z0-9]+\.[a-zA-z0-9]+$/;
var letter_regexp = /^[a-zA-zа-яА-Я\-]+$/;
var number_regexp =  /^[0-9]+$/;  

function checkPasswords(p1, p2)
{
    setState('passwords', (p1 == p2) && (p1 != ''));
}   

function setState(name, state)
{
    document.getElementById(name + '-wrong').style.display = state ? 'none' : '';
	document.getElementById(name + '-right').style.display = state ? '' : 'none';   
}

function addError(text)
{
    var errorDiv = document.getElementById('error_div');
    errorDiv.style.display = "";
	errorDiv.innerHTML = errorDiv.innerHTML + text + "<br>";
}

function checkRegisterErrors()
{
    var errorDiv = document.getElementById('error_div');
    errorDiv.innerHTML = "";
	errorDiv.style.display = "none";
    
    var error = false;

    var email = document.getElementById('email').value;
    var password1 = document.getElementById('password').value;
    var password2 = document.getElementById('password2').value;
    var name = document.getElementById('name').value;
    var surname = document.getElementById('surname').value;
    var birth_day = document.getElementById('birth_day').value;
    var birth_month = document.getElementById('birth_month').value;
    var birth_year = document.getElementById('birth_year').value;
    var private_number = document.getElementById('private_number').value;
    
    if(email_regexp.test(email) == false)
    {
        error = true;
        addError('Неправильно задан E-Mail');
    }
    if(number_regexp.test(private_number) == false)
    {
        error = true;
        addError('Личный номер должен состоять из цифр');
    }
    if(private_number.length != 7)
    {
        error = true;
        addError('Личный номер должен состоять из 7 цифр');
    }
    if(password1 != password2)
    {
        error = true;
        addError('Пароли не совпадают');
    }
    if(password1 == '')
    {
        error = true;
        addError('Не указан пароль');
    }
    if(name == '')
    {
        error = true;
        addError('Не указано имя');
    }
    else {
        if(letter_regexp.test(name) == false)
        {
            error = true;
            addError('Имя должно состоять из букв');
        }
    }
    if(surname == '')
    {
        error = true;
        addError('Не указана фамилия');
    }
    else {
        if(letter_regexp.test(surname) == false)
        {
            error = true;
            addError('Фамилия должна состоять из букв');
        }
    }
           
    if(birth_day == '0' || birth_month == '0' || birth_year == '0')
    {
        error = true;
        addError('Не указана дата рождения');
    }

    return error;
}


function checkEditProfileErrors()
{
    var errorDiv = document.getElementById('error_profile_div');
    errorDiv.innerHTML = "";
	errorDiv.style.display = "none";
    
    var error = false;

    var email = document.getElementById('email').value;
    var password1 = document.getElementById('password_new').value;
    var password2 = document.getElementById('password_new2').value;
    
    if(email_regexp.test(email) == false)
    {
        error = true;
        addError('Неправильно задан E-Mail');
    }
    if(password1 != password2)
    {
        error = true;
        addError('Пароли не совпадают');
    }
    return error;
}
