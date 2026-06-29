class DatasetExplorer:

    @staticmethod
    def dataset_info(df):

        print("\n========== TRANSFORMED DATA ==========\n")

        print("Rows :", df.shape[0])

        print("Columns :", df.shape[1])

        print("\nColumns\n")

        print(df.columns.tolist())