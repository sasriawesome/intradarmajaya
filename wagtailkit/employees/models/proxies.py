from modelcluster.models import ClusterableModel

from .employee import Employee


class EmployeeProxy(Employee):
    class Meta:
        proxy = True