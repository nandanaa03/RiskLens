class ETLReport:

    @staticmethod
    def generate(before_df, after_df):

        report = {

            "Rows Before": before_df.shape[0],

            "Rows After": after_df.shape[0],

            "Duplicates Removed":
                before_df.duplicated().sum(),

            "Missing Values Before":
                before_df.isnull().sum().sum(),

            "Missing Values After":
                after_df.isnull().sum().sum()
        }

        return report