# ACTSE-test task
## Essential Services:
1. JotForm (https://eu.jotform.com/)
2. Make.com (https://www.make.com/)
3. PipeDrive (https://www.pipedrive.com/)
4. Python + requests
5. Python library - smtplib (optional)
6. OpenAI API

## Task:

You need to build a flow that allows you to perform customer registration for a business.
The customer enters the created custom form and enters personal data (FirstName, LastName, Email, Phone). As a result of filling - form data should create a Contact in PipeDrive CRM.

After the contact gets into PipeDrive CRM, the system should extract his name and use artificial intelligence to determine the country (example: Jose Lopez = Spain) and place the country in the Organization field in PipeDrive CRM. The Email about successful registration should be sent to the customer using his native language.
