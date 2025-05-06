USAGE = """
This script converts a tolls.csv to tolls.dbf. 

Created for use in the NetworkProject No_missing_tolls.
Uses geopandas because other NetworkProjects already use geopandas so the dependency is not new.

See: Add a tolls.csv verification feature to NetworkWrangler
     https://app.asana.com/1/11860278793487/project/13098083395690/task/1203117964403499?focus=true
     Remove R dependency from NetworkWrangler tolls check
     https://app.asana.com/1/11860278793487/project/15119358130897/task/1210166332684908?focus=true
"""
import argparse, sys, traceback
import pandas
import geopandas

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=USAGE, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tolls_csv",  help="Input csv file")
    parser.add_argument("tolls_dbf", help="Output dbf file")
    my_args = parser.parse_args()

    df = pandas.read_csv(my_args.tolls_csv)
    gdf = geopandas.GeoDataFrame(df)
    gdf.to_file(my_args.tolls_dbf)
    print(f"Wrote {len(df)} records to {my_args.tolls_dbf}")
    sys.exit(0)
