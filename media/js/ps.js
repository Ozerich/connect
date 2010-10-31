/*
* Скрипт для отображения индикатора сложности пароля
*
* Made by Ozerich <OziCoder@gmail.com>

*/

function createPSIndicator(passwordInput, containerDiv, min, max, showText)
{
	if(min == null)
	if(min == null)
		min = 0;
	if(max == null)
		max = 25;
	if(showText == null)
		showText = true;
	var container = document.getElementById(containerDiv);
	container.className = "ps_container";
	var input = document.getElementById(passwordInput);
	
	var indicator_out = document.createElement("DIV");
	indicator_out.className = "ps_indicator_container";
	
	var indicator = document.createElement("DIV");
	indicator.className = "ps_indicator";
	
	var textDiv = document.createElement("DIV");
	textDiv.className = "ps_text";
	
	indicator_out.appendChild(indicator);
	container.appendChild(indicator_out);
	container.style.display = "";
	
	if(showText)
		container.appendChild(textDiv);


    var numeric = "0123456789";
    var lower = "abcdefghijklmopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя";
    var upper = "ABCDEFGHIJKLMOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ";
    var signs = "~`!@#$%^&*+-=_|\\/()[]{}<>,.;:?\"\'";
	
	function display(indicator, textDiv, strength, text)
	{
		var level;
		if(strength <= 40)level = 1;
		else if(strength <= 90)level = 2;
		else level = 3;
		if(text == null)
		{
			if(strength <= 40)text = "Легкий пароль";
			else if(strength <= 90)text = "Cредний пароль";
			else text = "Оптимальный пароль";
		}
		indicator.className = "ps_indicator ps_i_level" + level;
		indicator.style.width = strength + "%";
		textDiv.className = "ps_text ps_t_level" + level;
		textDiv.innerHTML = text + "<br>";
	}
	
	display(indicator, textDiv, 0, "Пустой пароль");
	
	var k = 1;
	k = k + 1;
	input.onkeyup = function()
	{
		var numeric_exist = false;
		var lower_exist = false;
		var upper_exist = false;
		var signs_exist = false;
		var numeric_count = 0;
		var only_numeric = true;
		var strengthValue = 0;
		textDiv.innerHTML = "";
		var value = input.value;
		
		if(value.length == 0)
		{
			display(indicator, textDiv, 0, "Пустой пароль");
			return;
		}
		
				if(value.length < min)
		{
			display(indicator, textDiv, 0, "Слишком короткий");
			return;
		}
		
		for(var i = 0; i < value.length; i++)
		{
			numeric_exist |= numeric.indexOf(value.charAt(i)) >= 0;
			lower_exist |= lower.indexOf(value.charAt(i)) >= 0;
			upper_exist |= upper.indexOf(value.charAt(i)) >= 0;
			signs_exist |= signs.indexOf(value.charAt(i)) >= 0;
		}
		
		numeric_only = !(lower_exist || upper_exist || signs_exist);
		if(numeric_only)
		{
			display(indicator, textDiv, 40);
			return;
		}
	
		if(value.length > max)
		{
			display(indicator, textDiv, 95);
			return;
		}
		
		strengthValue = (value.length / max).toString().substr(0,4);
		
		if(lower_exist || upper_exist)
			strengthValue = parseFloat(strengthValue) + 0.10;
		if(lower_exist && upper_exist)
			strengthValue = parseFloat(strengthValue) + 0.15;
		if(signs_exist)
			strengthValue = parseFloat(strengthValue) + 0.15;
		
		if(strengthValue > 0.95)
			strengthValue = 0.95;
		
		display(indicator, textDiv, strengthValue * 100);
	}
}

