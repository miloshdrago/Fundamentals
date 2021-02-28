# dependencies
import pandas as pd
from descartes import PolygonPatch
from shapely.geometry import Polygon

class Locations(object):
    """
    Utility class for dealing with geo data based on
    the twitter data set.

    @note           This class relies heavily on the structure
                    of the dataset for the first FDS assignment.
                    Thus, a very specific one-trick-pony class.

    @example        ```
                    # new instance of locations handler
                    locations = Locations('path/to/dataset.json')

                    # get all places as dataframe
                    places_df = locations.places()

                    # get only cities
                    places_cities_df = locations.places(place_type="city")

                    # get all polygon values of cities only with red colours (for plotting)
                    polygons = locations.polygons(place_type="city", fc="tomato")
                    ```

    @dependencies   pandas, descartes, shapely
    @author         Tycho Atsma <tycho.atsma@student.uva.nl>
    @file           Locations.py
    @documentation  public
    @copyright      University of Amsterdam
    """

    def __init__(self, path):
        """
        Constructor.
        @param  string  Path to JSON data set.
        """
        self._df = pd.read_json(path, lines=True)

    def places(self, **kwargs):
        """
        Method to get a dataframe of all places.
        @param  variadic    Supported keyword arguments:
                            "place_type": "admin", "city", "country".
        @return pandas.DataFrame
        """
        places = self._df['place']

        # handle given place type
        if kwargs['place_type']:
            df = pd.DataFrame([pd.Series(e) for e in places if e['place_type'] == kwargs['place_type']])

        # handle all place types
        else:
            df = pd.DataFrame([pd.Series(e) for e in places])

        # expose a sub dataframe that only contains place data
        return df

    def coordinates(self, place_type=None):
        """
        Method to get a list of coordinates based on the places.
        @param  string  Type of place (optional).
                        Supports: "place_type": "admin", "city", "country".
        @return list
        """
        places = self.places(place_type=place_type)
        
        # expose a list of coordinates only
        return [place['coordinates'][0] for place in places['bounding_box']]

    def polygons(self, place_type=None, **kwargs):
        """
        Method to get a list of polygons based on the coordinates of all places.
        @param  string      Type of place (optional).
                            Supports: "place_type": "admin", "city", "country".
        @param  variadic    Supported keyword arguments:
                            "place_type": "admin", "city", "country".
                            Arguments for `descartes.PolygonPatch`
        @return list
        """
        places = self.coordinates(place_type=place_type)

        # expose a list of polygons only
        return [PolygonPatch(Polygon(place), **kwargs) for place in places]
