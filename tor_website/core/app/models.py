from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=2, unique=True)
    svg_path = models.TextField()  # SVG path for the state's shape

    def __str__(self):
        return self.name

class County(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, related_name='counties', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.state.name}"

class Post(models.Model):
    county = models.ForeignKey(County, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post in {self.county.name} at {self.timestamp}"
