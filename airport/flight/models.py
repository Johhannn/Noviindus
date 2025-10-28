from django.db import models

class Route(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def total_duration(self):
        """Returns total duration (sum of all nodes’ durations)."""
        return sum(node.duration for node in self.nodes.all())

    def __str__(self):
        return self.name


class AirportNode(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='nodes')
    airport_code = models.CharField(max_length=10)
    position = models.PositiveIntegerField()
    duration = models.FloatField(help_text="Duration in minutes (to next node)")

    class Meta:
        unique_together = ('route', 'position')
        ordering = ['route', 'position']

    def __str__(self):
        return f"{self.route.name} | {self.position}: {self.airport_code} ({self.duration}m)"
