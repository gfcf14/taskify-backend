# Taskify Backend

This repository is the backend part of my Taskify project.

## Description
The Taskify project represents a simple web application which supports authentication, project creation, and creation of different tasks assigned to a project, both able to be modified to indicate status of completion (To do, Active, Review, and Complete).

## Purpose

The idea I had through making this project was to demonstrate the basic CRUD operations available in a Python backend application, as supported via the Django framework.

## Installation
If you're pulling this repo, a virtual environment will be required. Create one via:

```sh
python3 -m venv venv
```
Then activate it for use with the repo by calling `source venv/bin/activate` or `venv\Scripts\activate` if on Windows.
Since this repo already contains requirements, it should be enough to call the following:
```sh
pip install -r requirements.txt
```
Which will install all the requirements for this app in the virtual environment. Once this is done, perform the following:
```python
python manage.py migrate
python manage.py runserver
```
To setup the database and run the app. Be sure to create a **.env** file to specify a database, user, password, host and port.

## Application Flow
![enter image description here](https://github.com/gfcf14/taskify-backend/blob/main/taskify_flowchart.png?raw=true)

The application flow is simpler than displayed. In the beginning the user authentication token is checked. If not valid (whether expired or nonexistent) the user is directed to the login page. Upon successful login, the user is directed to the **/dashboard** page, which in the backend fetches all existing projects from **/api/projects/**, if any exist. When clicking on any existing project the user is taken to the project page, where tasks by project are fetched by hitting the **/projects/:id** endpoint. When creating, updating, or deleting any of the new or existing projects the list in which they are displayed is updated to show changes. Lastly, for any of these changes the token is checked, and if it is found to be expired, the user is directed to the login page again to obtained a new token.

## Features

- **Basic authentication via Simple JWT:** When the user navigates to **api/token/** the **rest_framework_simplejwt** view checks if the provided credentials are valid, as per the implementation for the path `path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),` . When valid, an authorization token is returned.
- **Database record read:** The route **api/projects/** (also when specifying a project id) calls a project view, which contains custom implementation of several basic CRUD functions:
```python
class  ProjectView(generics.GenericAPIView):
	queryset = Project.objects.all()
	serializer_class = ProjectSerializer  

	def  get(self, request, *args, **kwargs):
		queryset = Project.objects.all()
		serializer_class = ProjectSerializer

		if  'pk'  in kwargs:
			project_id = kwargs['pk']
			tasks = Task.objects.filter(project=project_id)
			serializer =  TaskSerializer(tasks, many=True)
		else:
			projects = Project.objects.all()
			serializer =  ProjectSerializer(projects, many=True)

		return  Response(serializer.data, status=status.HTTP_200_OK)

	def  post(self, request, *args, **kwargs):
		serializer =  ProjectSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()

			return  Response(serializer.data, status=status.HTTP_201_CREATED)

		return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def  patch(self, request, *args, **kwargs):
		project =  self.get_object()
		serializer =  ProjectSerializer(project, data=request.data, partial=True)
		
		if serializer.is_valid():
			serializer.save()
			
			return  Response(serializer.data, status=status.HTTP_200_OK)

	def  delete(self, request, *args, **kwargs):
		project = Project.objects.get(id=kwargs['pk'])
		project.delete()

		return  Response(status=status.HTTP_204_NO_CONTENT)
```
The **get** function intends to initially fetch from the Project serializer, but if a **pk** param is provided, the program will understand it needs to fetch Tasks instead. As such in such a case the serializer is changed to Tasks and these are fetched by the param provided, which is the Project id.

- **Database record creation:** The implementation of **post** makes it simple to first serialize the incoming data to understand which type must be saved, and if it's valid it gets inserted into the database.
- **Database record update:** Update is taken care of via the **patch** implementation, which fetches a Project object from the incoming data, even checking if the update is partial. If valid, proceed with the update.
- **Database record deletion:** Deletion is handled via the **delete** function, which is as simple as fetching and deleting the project via the **id** provided (the pk param). The importance of this delete functionality is understated in the simplicity of the code, as visible through the Task model:
```python
class  Task(models.Model):
	STATUS_CHOICES  = [
		(0, 'TODO'),
		(1, 'ACTIVE'),
		(2, 'REVIEW'),
		(3, 'COMPLETE'),
	]  

	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	description = models.TextField()
	status = models.IntegerField(choices=STATUS_CHOICES, default=0)
	created_at = models.DateTimeField(auto_now_add=True) 

	def  __str__(self):
		return  self.title
```

Note the **project** property is specified as a foreign key, with the **on_delete** property set to **cascade**. Once a Project is deleted, the database will be able to delete all associated tasks.
