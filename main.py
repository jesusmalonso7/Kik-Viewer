from Kik_Functions import KikProcessing
import send2trash



if __name__ == '__main__':

    # path to conversations.csv
    csv_file = 'C:/Users/jesus/Desktop/test_files/conversations.csv'
    my_process = KikProcessing(csv_file)
    new_csv = my_process.remove_snapchat_legend_from_csv_file(csv_file)
    users = my_process.get_users(new_csv)  # Dictionary of all Snapchat users in this return
    # Get information for a specific user
    username, user_id = my_process.get_user(users, '0a8f089b-1a37-41f9-ad9c-5584d790d9bc')
    #my_process.print_chats(username, new_csv)
    my_process.get_chat(user_id, new_csv)
    send2trash.send2trash('C:\\Users\\jesus\\Desktop\\test_files\\output.csv')