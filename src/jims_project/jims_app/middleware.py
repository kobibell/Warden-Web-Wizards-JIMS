class ClearSessionDataMiddleware:
    """
    Middleware to clear session data related to the forms when the user navigates
    away from any path under the 'add-inmate/' path.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware with the get_response function.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        This method is called for each request. It checks if the request path does
        not start with '/add-inmate/' and clears the related session data if necessary.
        """
        
        # Call the get_response function to get the response
        response = self.get_response(request)

        # Check if the request path does not start with '/add-inmate/'
        if not request.path.startswith('/add-inmate/'):
            # Remove the 'inmate_traits_data' from the session if it exists
            request.session.pop('inmate_traits_data', None)

            # Remove the 'inmate_arrest_info_data' from the session if it exists
            request.session.pop('inmate_arrest_info_data', None)

            # Remove the 'inmate_health_sheet_data' from the session if it exists
            request.session.pop('inmate_health_sheet_data', None)

        # Return the response
        return response
