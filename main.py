#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

page_header = '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>STLCC - LC101 - User Signup</title>
            <style type="text/css">
                .error {
                    color: red;
                }
                label {
                    text-align: right;
                    display: block;
                }
            </style>
        </head>
        <body>
'''

page_footer = '''
        </body>
    </html>
'''

def pageSetup(thisUser, thisEmail, userError, passError, verifyError, emailError):
    up_content = '''
            <h2>User Signup - STLCC LC101</h2>
            <form method="post">
                <table>
                    <tr>
                        <td>
                            <label for="username">Username: </label>
                        </td>
                        <td>
        '''
    formUser = '                    <input type="text" name="username" value="' + thisUser +'" required /> '
    split_content = '''
                        </td>
                        <td>
    '''
    userErr = '                        <span class="error">' + userError + '</span>'
    mid_content = '''
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="password">Password: </label>
                        </td>
                        <td>
                            <input type="password" name="password" value="" required />
                        </td>
                        <td>
        '''
    passErr = '                    <span class="error">' + passError + '</span>'
    low_content = '''
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="verification">Verify Password:  </label>
                        </td>
                        <td>
                            <input type="password" name="verification" value="" required />
                        </td>
                        <td>
    '''
    verErr = '                        <span class="error">' + verifyError + '</span>'
    bot_content = '''
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="email">Email <em>(optional)</em>:  </label>
                        </td>
                        <td>
    '''
    emlUser = '                    <input type="text" name="email" value="' + thisEmail +'" /> '
    emlUser2= '''
                        </td>
                        <td>
    '''
    emlErr = '                        <span class="error">' + emailError + '</span>'
    base_content = '''
                        </td>
                    </tr>
                </table>
            <br />
            <input type="submit" value="Submit"/>
        </form>
    '''
    formed_up = formUser + split_content + userErr + mid_content + passErr
    formed_on = formed_up + low_content + verErr + bot_content + emlUser + emlUser2 + emlErr
    form_content = page_header + up_content + formed_on + base_content + page_footer

    return form_content


class MainHandler(webapp2.RequestHandler):
    def get(self):
        thisUser = ""
        thisEmail = ""
        userError = ""
        passError = ""
        verifyError = ""
        emailError = ""
        content = pageSetup(thisUser, thisEmail, userError, passError, verifyError, emailError)
        self.response.write(content)

    def post(self):
        thisUser = ""
        thisEmail = ""
        userError = ""
        passError = ""
        verifyError = ""
        emailError = ""
        doubleCheck = False

        thisUser = self.request.get("username")
        if re.match(r"^[a-zA-Z0-9_-]{3,20}$", thisUser) is None:
            userError = "This is not a valid username"
            doubleCheck = True

        thisPass = self.request.get("password")
        if re.match(r"^.{3,20}$", thisPass) is None:
            passError = "This is not a valid password"
            doubleCheck = True

        thisVerify = self.request.get("verification")
        if thisPass != thisVerify:
            verifyError = "The passwords do not match"
            doubleCheck = True

        thisEmail = self.request.get("email")
        if thisEmail != "" and re.match(r"^[\S]+@[\S]+[.][\S]+$", thisEmail) is None:
            emailError = "This is not a valid email address"
            doubleCheck = True

        if doubleCheck is True:
            content = pageSetup(thisUser, thisEmail, userError, passError, verifyError, emailError)
            self.response.write(content)
        else:
            self.redirect("/welcome" + "?username=" + thisUser)



class WelcomeUser(webapp2.RequestHandler):
    def get(self):
        thisUser = self.request.get("username")
        if re.match(r"^[a-zA-Z0-9_-]{3,20}$", thisUser) is None:
            self.redirect("/")
        else:
            message = '<h2>Welcome, ' + thisUser + '!</h2>'
            content = page_header + message + page_footer
            self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeUser)
], debug=True)
