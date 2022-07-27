# Genesis API Test Task
Цей репозиторій створений для тестовго завдання для "Genesis Software engineering school". 
Він представляє собою API створене за допомогою фреймворку Flask, яке дозволяє дізнатись поточний курс Біткоіну в гривнях, 
підписати наданий email для розсилки курсу Біткоіну та розіслати цю інформацію на підписані email'и. 
Отримання курсу проходить через API [Kuna.io](https://kuna.io)

## Installation and runnning
1. Клонувати чи скачати репозиторій 
2. Збудувати докер: *docker build --tag python-docker .*
3. Запустити отриманий docker image в detached mode: *docker run -d -p 5000:5000 python-docker*

## User guide
### 1. Отримання поточного курсу BTC
**GET** request на url: *http://127.0.0.1:5000/api/rate*

**Responses**:
- Code: *200*.  Message: *нинішній BTCUAH курс*.
- Code: *400*.  Message: *Invalid status value*.  Description: *можлива помилка в API Kuna*
### 2. Додання нового email'у до підписок
**POST** request на url: *http://127.0.0.1:5000/api/subscribe?email=<your_email@exmp.com>*

**Responses**:
- Code: *200*.  Message: *E-mail додано*.
- Code: *400*.  Message: *No email provided*. Description: *ви не передали email в запиті*.
- Code: *406* : Message: *Email has incorrect format. Enter a valid email*. Description: *ви передали email в неправильному форматі*.
- Code: *409* : Message: *Email already exists*. Description: *цей email вже є в базі*.
### 3. Додання нового email'у до підписок
Для відправки листів використовується спеціально зроблена мною поштова адреса, яка використовується лише для цілей цього API.
**POST** request на url: *http://127.0.0.1:5000/api/sendEmails*

**Responses**:
- Code: *200*.  Message: *E-mailʼи відправлено*.
- Code: *401*.  Message: *Error occured while logging into smtp server*. Description: *сталася помилка при вході в пошту, з якої надсилається лист*.
- Code: *418* : Message: *An error occured while SMTP_SSL connection.*. Description: *при роботі поштового серверу сталася помилка*.
### 4. Зміна пошти відправника 
У разі якщо виникла потреба змінити пошту з якої надходять листи, потрібно використовувати цей запит 
**PUT** request на url: *http://127.0.0.1:5000/api/sendEmails?email=new_email@exmp.com&password=your_pass*

**Responses**:
- Code: *200*.  Message: *smtp_server was succefully updated*.
- Code: *400*.  Message: *No smtp_server provided*. Description: *ви не передали нову пошту в запиті*.
- Code: *400*.  Message: *No password provided*. Description: *ви не передали новий пароль в запиті*.

# Коментарі до логіки роботи
Увесь код знаходиться в файлі *app.py*.

На початку файлу йдуть функції, які використвовуються багатьма функціями: *checkEmail* - перевіряю чи правильний формат введеного email'у 
та *getTickers* - отримує ціну біткоіна в гривнях з Куна. Остання функція спеціально зроблена так, щоб потенційно вона могли приймати декілька монет та валют.

Клас *Rate* відповідає за повернення поточного курсу Біткоіна та має лише метод *get*.

Клас *Subscription* відповідає за додавання нового email'у до підписок та має лише метод *post*.

Клас *Sender* відповідає за надсилання листів та зміну пошти відправника. Перше реалізується в *post*, а друге в *put* запиті.
