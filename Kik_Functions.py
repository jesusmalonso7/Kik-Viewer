import pandas as pd
import csv
import os

# Requires the following packages: pandas, csv, os


class KikProcessing:
    def __init__(self, conversation_fp: str):
        self.conversation_fp = conversation_fp

    @staticmethod
    def get_user(user_list: list, find_user: str) -> list:
        """
           @param: user_list is a python list object that contains all the usernames for this account
           @param: find_user is the username needed to find a specific user in the user list.
           @return: A list of account usernames
        """
        for u_name in user_list:
            if find_user == u_name:
                break
        return u_name

    @staticmethod
    def get_csv_header(conversation_fp: str) -> (int, list):
        """
            @param: conversation_fp: path to original CSV file.
            @return: A tuple with an integer value identifying the row on which the CSV header is found, and a list
                     containing the header values.
        """
        # Counter
        num_rows_before_header = 0
        # Will hold the Kik CSV header from the CSV file
        header = ''
        with open(conversation_fp, encoding='utf-8') as input_file:
            for row in input_file:
                # Create a list
                row = row.split(',')
                # Count how many rows have been processed by adding one (1) for iteration of the for loop
                num_rows_before_header += 1
                # Once the row containing content_type has been found, the header has been identified.
                if row[0] == 'msg_id':
                    # Get a copy of the header
                    header = row
                    break
        # Python starts counting from 0. Subtract one to correct for this in num_rows_before_header.
        return num_rows_before_header - 1, header

    @staticmethod
    def get_users(output_fp: str) -> list:
        """
            @param: output_fp: path to Kik CSV file.
            @return: List of users
        """
        # Build DataFrame from the provided CSV file.
        df = pd.read_csv(output_fp, encoding='utf-8', dtype=str)
        # Create a list of all the users present in the Kik CSV file. The list has duplicates
        u_name = df['sender_jid'].to_list()
        # Remove the duplicates
        u_name = list(dict.fromkeys(u_name))
        # Sort users in alphabetical order
        u_name.sort()
        return u_name

    def remove_kik_legend_from_csv_file(self, conversation_fp: str) -> str:
        """
            @param: conversation_fp: path to original Kik CSV.
            @return: A filepath to a new Kik CSV file.

        """
        # Returns the header and index where the header was found. The header is not being used here
        header_index, _ = self.get_csv_header(conversation_fp)
        # create the filepath for the output CSV file using the current working directory
        output_fp = os.path.join(os.path.dirname(conversation_fp), 'output.csv')
        # Open both, input and output, files
        with open(conversation_fp, encoding='utf-8', newline='') as input_fd, open(output_fp, 'w', encoding='utf-8',
                                                                          newline='') as output_fd:
            reader = csv.reader(input_fd)
            output = csv.writer(output_fd)

            for row_index, row in enumerate(reader):
                # Skip any lines present prior to header_index.
                if row_index >= header_index:
                    output.writerow(row)
        # Return a new csv file that only contains account data.
        return output_fp

    def get_chat(self, user_identifier: str, output_fp: str) -> list:
        """
           @param: user_identifier: The chat log for a specific user.
           @param: output_fp: The file path to the Kik CSV file.
           @param: write_to_file: If True, write the conversation log for a specific user to a file. Otherwise, only
                   return a list containing the conversation log.
           @return: List of chat logs sent between the account holder and other Kik users.
           @Descrip: Walk through the list of senders and print the chats for each sender.
        """
        # Use Pandas DataFrame to read the output.csv file.
        df = pd.read_csv(output_fp, encoding='utf-8', dtype=str)
        # Convert the values in the timestamp column to a Pandas datetime object
        df['sent_at'] = pd.to_datetime(df['sent_at'])
        # Sort the new output.csv file by the timestamp column
        df.sort_values('sent_at', inplace=True)
        # Remove all NAN (not a number) entries from the data frame.
        df = df.fillna(' ')
        # Contains a list of the chats
        log = []
        # Get the header and row index for the header. The row index is not being used here.
        _, header = self.get_csv_header(output_fp)
        # Add header as the first list string
        log.append(header)
        for index, row in df.iterrows():
            # Check for_user in the sender_username column and the recipient_username column to get all the entries for
            # that specific user. Note: for_user may be a sender at times and a recipient at others.
            if row['sender_jid'] == user_identifier:
                log.append(row.to_list())
            elif row['receiver_jid'] == user_identifier:
                log.append(row.to_list())
        return log

    def print_chats(self, for_username: str, output_fp: str):
        """
            @param: for_username: print chat logs for this user
            @param: output_fp: Path to the Kik CSV file
            @Descrip: Outputs a CSV file containing all the extracted chat conversations.
        """
        # Creat a filepath to the chatlog.csv using the current working directory
        with open(os.path.join(os.path.dirname(output_fp), f'{for_username}.csv'), 'w',
                  encoding='utf-8', newline='') as output_fd:
            output = csv.writer(output_fd, dialect='excel')

            # Get the header and row index for the header. The row index is not being used here.
            _, header = self.get_csv_header(output_fp)
            # Get the entire chat log for a specific user
            logs = self.get_chat(for_username, output_fp)
            for count, log in enumerate(logs, start=1):
                output.writerow(log)
                # print(log)
                # Add a header row every fifty entries
                if count % 50 == 0:
                    output.writerow('\n')
                    output.writerow(header)
