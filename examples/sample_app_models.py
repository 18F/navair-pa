from django.db import models


class MaintenanceEvent(models.Model):
    """ 
    Defines maintenance events in the life of a given aircraft, 
    which can roll up to the Aircraft Type and Platform levels.

    Given the hours on the aircraft, we can begin to predict when 
    other similar aircraft should expect to have issues.

    Ideally, these events can be populated based on information being 
    gathered and stored in other systems and these events are created according 
    to an automated, recurring job. If they are hand-entered, guard against errors, 
    especially in the maintenance_code field.

    It might also be useful or desirable to make maintenance_code a ForeignKey 
    to another DB table, in order to better track and chart different types of maintenance.
    """

    aircraft = models.ForeignKey('Aircraft', on_delete="CASCADE")
    hours = models.IntegerField(help_text="Number of hours on the aircraft.")
    maintenance_code = models.CharField(help_text="A unique identifier to track the type of maintenance done.")
    date = models.DateField()

    class Meta:
        ordering = ['aircraft', 'hours']


class Platform(models.Model):
    """
    Defines top aircraft platform.
    Example: P-3
    """
    name = models.CharField(max_length=200)
    description = models.TextField(help_text='Optional: General information about the platform.', blank=True)

    def __str__(self):
        return self.name

    def maintenance_events(self):
        """
        Returns all events that roll up to this platform
        """
        return MaintenanceEvent.objects.filter(aircraft__aircraft_type__platform=self)


class AircraftType(models.Model):
    """
    Defines a type of aircraft within a platform.
    Examples: P-3A, P-3B, P-3C
    """
    platform  = models.ForeignKey(Platform, on_delete="CASCADE")
    variant = models.CharField(max_length=10)
    name    = models.CharField(max_length=200, blank=True)
    notes   = models.TextField(blank=True)
    
    class Meta:
        unique_together = ("platform", "variant")

    def __str__(self):
        return "%s %s" % (self.platform, self.variant)

    def maintenance_events(self):
        return MaintenanceEvent.objects.filter(aircraft__aircraft_type=self)


class Aircraft(models.Model):
    """
    Defines an individual example of an AircraftType. In other words, 
    the actual aircraft, with a tail number.

    It may be useful to store other information here, 
    such as the unit or base assignment for the aircraft.
    """
    aircraft_type = models.ForeignKey(AircraftType, on_delete="CASCADE")
    tail_number = models.CharField("Tail Number", max_length=30, unique=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.tail_number

    def platform(self):
        return self.aircraft_type.platform
    
    def maintenance_events(self):
        """
        Gets all maintenance events for this particular aircraft.
        This is already available through just following the relationship in the
        Django ORM, so this is just a convenience method to help keep the syntax
        consistent between the aircraft, aircraft_type and platform levels.
        """
        return self.maintenanceevent_set.all()
