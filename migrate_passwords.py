import sqlite3

#This function takes a dictionary password_mapping as input, where keys are user IDs, and values are the new plain-text passwords 
# that need to be stored in the database.
def migrate_passwords(password_mapping):
    conn = sqlite3.connect('users.db') #connecting to the database
    c = conn.cursor() #creating SQLite queries

    for user_id, new_plain_text_password in password_mapping.items():
        # Update the password in the database to the actual password
        c.execute('UPDATE users SET password=? WHERE id=?', (new_plain_text_password, user_id))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Replace the values in this dictionary with the actual user IDs and corresponding plain-text passwords
    password_mapping = {
        1: 'Andrew09',
        2: 'Andrew#09',
        3: 'Andrew#2009',
        4: 'Andrew22',
        5: 'Purplepancakes',
        6: 'Superman'
        # Add more entries as needed
    }

    migrate_passwords(password_mapping)
