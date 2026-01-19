from django.db import models

class Route(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def total_duration(self):
        """Returns total duration (sum of all nodes’ durations)."""
        return sum(node.duration for node in self.nodes.all())

    def __str__(self):
        return self.name


class FlightNode(models.Model):
    NODE_TYPE_CHOICES = (
        ('root', 'Root'),
        ('left', 'Left'),
        ('right', 'Right'),
    )

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='nodes')
    airport_code = models.CharField(max_length=10)
    duration = models.FloatField(help_text="Duration from parent node")
    
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_nodes')
    node_type = models.CharField(max_length=10, choices=NODE_TYPE_CHOICES, default='root')
    
    class Meta:
        unique_together = ('parent', 'node_type')

    def __str__(self):
        if self.parent:
            return f"{self.airport_code} ({self.node_type} of {self.parent.airport_code}, {self.duration}km/min)"
        return f"{self.airport_code} (Root)"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.node_type == 'root' and self.parent is not None:
            raise ValidationError("Root node cannot have a parent.")
        if self.node_type != 'root' and self.parent is None:
            raise ValidationError("Non-root node must have a parent.")

