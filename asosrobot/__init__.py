from productdetails import AsosProductDetailsJob
from catchproduct import AsosCatchProductJob


def register_plugin( pm ):
	pm.register("details.asos", AsosProductDetailsJob)
	pm.register("catch.asos", AsosCatchProductJob)

	
