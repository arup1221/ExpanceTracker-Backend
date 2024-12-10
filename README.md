# Api information

### Register api

```bash
http://127.0.0.1:8000/api/auth/register/
```

fields

```bash
{
    "email": "JohnDoe@example.com",
    "username": "John",
    "password": "johndoe2345",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": "True",
    "is_staff": "False"
}
```

### Login Api

```bash
http://127.0.0.1:8000/api/auth/login/
```

```bash
{
    "email": "JohnDoe@example.com",
    "password": "johndoe2345"
}
```

### Category Apis

```bash
http://127.0.0.1:8000/api/expenses/categories/
```

GET - to get all category

```bash
[
    {
  "id": 1,
  "name": "Food",
  "description": "Food and dining expenses"
}
]
```

POST - to add Category

```bash
{
  "name": "Travel",
  "description": "Traveling cost"
}
```

```bash
http://127.0.0.1:8000/api/expenses/categories/<id>
```

GET- specific category

### Expense Apis

```bash
http://127.0.0.1:8000/api/expenses/expenses/
```

GET - get all expences

```bash
[
  {
    "id": 1,
    "user": "John",
    "category": "Food",
    "title": "Grocery Shopping",
    "amount": "150.00",
    "date": "2024-11-04",
    "description": "Bought groceries for the week"
  }
]
```

POST - to add expences

```bash
{
  "category": "Food",
  "title": "Grocery Shopping",
  "amount": "150.00",
  "description": "Bought groceries for the week"
}

```

### Recurring Apis

```bash
http://127.0.0.1:8000/api/expenses/recurring-expenses/
```

GET - get all recurring expences

```bash
[
  {
    "id": 1,
    "expense": 1,
    "interval": "Monthly",
    "next_due_date": "2025-01-01"
  },
]
```

POST - post any recurreing expence

```bash
{
  "expense_id": 1,
  "interval": "Weekly",
  "next_due_date": "2024-10-01"
}
```

### Budget Apis

```bash
http://127.0.0.1:8000/api/expenses/budgets/
```

GET - get all budget details

```bash
[
  {
    "id": 1,
    "user": "John",
    "category": "Food",
    "limit": "1000.00",
    "start_date": "2024-11-01",
    "end_date": "2024-11-30",
    "amount_spent": "150.00"
  },
]
```

POST - give the budget details

```bash
{
  "category": "Travel",
  "limit": "2000.00",
  "start_date": "2024-11-05",
  "end_date": "2024-12-01"
}
```

### Summery Api

```bash
http://127.0.0.1:8000/api/expenses/summary/
```

GET - get the summary of previos

```bash
{
  "total_expense": 1849.0,
  "today_expense": 0,
  "last_day_expense": 0,
  "current_week_expense": 1849.0,
  "last_week_expense": 0,
  "current_month_expense": 1849.0,
  "last_month_expense": 0,
  "current_year_expense": 1849.0,
  "last_year_expense": 0
}
```