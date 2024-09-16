# expense-tracker
This is my project to manage expenses
You can see the project detail and requirement in this link: https://roadmap.sh/projects/expense-tracker
This project have some functionality like:
- Users can add an expense with a description and amount.
- Users can update an expense.
- Users can delete an expense.
- Users can view all expenses.
- Users can view a summary of all expenses.
- Users can view a summary of expenses for a specific month (of current year).
- Add expense categories and allow users to filter expenses by category.
- Allow users to export expenses to a CSV file.

I use Python, argparse to handle cli, pandas to export csv.

*you can check all command in this project by* `py main.py --help`
![image](https://github.com/user-attachments/assets/e1119f4c-ff5b-4bb1-9501-16558e579161)

## Add new expense
**py main.py add --description "your description" --amount 77 --category food**
- amount is required in this functionality
  
  ![image](https://github.com/user-attachments/assets/bd70dcd2-b554-4da6-b794-d89be0a612b7)


## Update exist expense
**py main.py update --id 6 --amount 4**

![image](https://github.com/user-attachments/assets/1486b3a0-c9e5-4055-a173-682fad61b135)

## Delete a expense
**py main.py delete --id 6**

![image](https://github.com/user-attachments/assets/f487da60-1ec8-41e6-87f7-261acf14e728)

## List all expenses
**py main.py list**

![image](https://github.com/user-attachments/assets/636d66b2-72ee-4e48-9a81-0657a329575e)

## Summary of all expenses
**py main.py summary**

![image](https://github.com/user-attachments/assets/4dfde5be-6141-423b-9b6a-c0ba8f6194c3)

## Summary of expenses for a secific month
**py main.py summary --month 9**

![image](https://github.com/user-attachments/assets/e0d25988-5325-487b-9548-6d672f7db71a)

## Add category and list all catogories
**py main.py list_category**

![image](https://github.com/user-attachments/assets/88b8177a-e723-4684-826b-5b87d54c8e11)

`py main.py add_category --category transportation`

![image](https://github.com/user-attachments/assets/267aeb2f-5ecc-4dc2-8c9f-71c7b466acfc)

## Export all expenses
**py main.py export**

![image](https://github.com/user-attachments/assets/e368a650-ae96-4ed8-a125-77ffac252902)

![image](https://github.com/user-attachments/assets/255f04d8-2979-49ca-bea8-8d8872f45ed9)
