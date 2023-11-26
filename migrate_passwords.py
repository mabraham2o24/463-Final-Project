import sqlite3

def migrate_passwords(password_mapping):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    for user_id, new_plain_text_password in password_mapping.items():
        # Update the password in the database
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
