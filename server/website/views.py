from datetime import date
from flask import Blueprint, request, jsonify
from . import auth
from .models import Company, Developers, Contracts, Applications, PrefLang, Blocked, Experience
from . import db

views = Blueprint('views', __name__)


#####################################################
#               Company Dashboard                   #
#####################################################
@views.route("/CompanyDash", methods=['POST', 'GET'])
def company_dash():
    if request.method == 'GET':
        # Get logged-in user:
        user_key = auth.decode_token(request.headers['tok'])

        # Check if user is valid
        if user_key == -1:
            response = {
                'status': 'fail',
                'message': 'Invalid or missing token'
            }
            return jsonify(response, 403)

        # Send all data to dashboard:
        try:
            com = Company.query.filter_by(CompID=user_key).first()
            contr = Contracts.query.filter_by(CompID=user_key).all()
            open_contr = Contracts.query.filter_by(CompID=user_key, Status='Open').all()
            close_contr = Contracts.query.filter_by(CompID=user_key, Status='Closed').all()
            money_spent = 0
            for row in close_contr:
                money_spent += row.Value

            # Dictionaries:
            contr_dicts = contracts_to_dict(contr)
            open_contr_dicts = contracts_to_dict(open_contr)
            close_contr_dicts = contracts_to_dict(close_contr)

            response = {
                'CompanyDetails': {'CompanyName': com.CompanyName, 'Email': com.Email, 'MoneySpent': money_spent,
                                   'GeneralIndustry': com.GeneralIndustry, 'Bio': com.Bio, 'Logo': com.Logo},
                'Contracts': contr_dicts,
                'OpenContracts': open_contr_dicts,
                'ClosedContracts': close_contr_dicts,
            }
            return jsonify(response, 200)
        except:
            response = {
                'status': 'fail',
                'message': 'Database error.'
            }
            return jsonify(response, 400)


@views.route("/CompanyDash/viewContract", methods=['POST', 'GET', 'PUT'])
def view_contract():
    if request.method == 'GET':
        # get contract ID
        contr_id = request.headers['contract_id']

        # Get applications of contract:
        try:
            applications = Applications.query.filter_by(ContractID=contr_id).all()
            appli_list = []
            for filt in applications:
                if Developers.query.filter_by(DevID=filt.DevID, Status='Available').first() is not None:
                    appli_list.append(filt)

            i = 1
            applications_dict = {}
            applicant_dict = {}
            for row in appli_list:
                applicant = Developers.query.filter_by(DevID=row.DevID).one()
                lang = Experience.query.filter_by(DevID=row.DevID).all()
                lang_list = []
                for result in lang:
                    lang_list.append(result.Language)

                applicant_dict[i] = {'DeveloperID': row.DevID, 'Username': applicant.Username, 'Status': applicant.Status,
                                     'Experience': applicant.Experience, 'Avatar': applicant.UserAvatar,
                                     'Email': applicant.Email, 'Languages': lang_list, 'ApplyStatus': row.ApplyStatus}
                i = i + 1
            response = {
                'applications': applications_dict,
                'applicantDet': applicant_dict,
            }
            return jsonify(response, 200)
        except:
            response = {
                'status': 'fail',
                'message': 'Database error.'
            }
            return jsonify(response, 400)


@views.route("/CompanyDash/ContractApplication", methods=['GET', 'PUT'])
def company_accept_decline():
    if request.method == 'PUT':
        put = request.get_json()

        # Get values:
        contract_id = put.get('ContID')
        dev_id = put.get('DeveloperID')
        accept = put.get('Accepted')

        # Update application:
        try:
            if accept is True:
                appli_status = Applications.query.filter_by(DevID=dev_id, ContractID=contract_id).one()
                appli_status.ApplyStatus = 'Accepted'
                db.session.commit()

                appli_status = Applications.query.filter_by(ContractID=contract_id, ApplyStatus='Pending').all()
                for row in appli_status:
                    row.ApplyStatus = 'Declined'
                db.session.commit()

                contr = Contracts.query.filter_by(ContractID=contract_id).one()
                contr.Status = 'Closed'
                db.session.commit()

                response = {
                    'status': 'success',
                    'message': 'Successfully updated.'
                }
                return jsonify(response, 200)
            else:
                appli_status = Applications.query.filter_by(DevID=dev_id, ContractID=contract_id).one()
                appli_status.ApplyStatus = 'Declined'
                db.session.commit()
                response = {
                    'status': 'success',
                    'message': 'Successfully updated.'
                }
                return jsonify(response, 200)
        except:
            response = {
                'status': 'fail',
                'message': 'Database error.'
            }
            return jsonify(response, 400)


@views.route("/CompanyDash/profileEdit", methods=['GET', 'PUT'])
def company_dash_profile_edit():
    if request.method == 'GET':
        # Get logged-in user:
        user_key = auth.decode_token(request.headers['tok'])

        if user_key == -1:
            response = {
                'status': 'fail',
                'message': 'Invalid or missing token'
            }
            return jsonify(response, 403)

        comp = Company.query.filter_by(CompID=user_key).one()

        # Send data of user in response:
        response = {
            'CompanyName': comp.CompanyName,
            'Email': comp.Email,
            'GeneralIndustry': comp.GeneralIndustry,
            'Bio': comp.Bio,
            'Avatar': comp.Logo,
        }
        return jsonify(response, 200)
    elif request.method == 'PUT':
        put = request.get_json()

        # Save new data to be inserted:
        comp_name = put.get('CompanyName')
        comp_email = put.get('Email')
        comp_bio = put.get('Bio')
        comp_industry = put.get('GeneralIndustry')
        comp_avatar = put.get('Avatar')
        # Get logged-in user and update data:
        try:
            # Get logged-in user:
            user_key = auth.decode_token(request.headers['tok'])
            if user_key == -1:
                response = {
                    'status': 'fail',
                    'message': 'Invalid or missing token'
                }
                return jsonify(response, 403)

            company = Company.query.filter_by(CompID=user_key).one()
            company.CompanyName = comp_name
            company.Email = comp_email
            company.Bio = comp_bio
            company.GeneralIndustry = comp_industry['name']
            company.Logo = comp_avatar

            db.session.commit()
            response = {
                'status': 'success',
                'message': 'Successfully updated.'
            }
            return jsonify(response, 200)
        except:
            response = {
                'status': 'fail',
                'message': 'Database error.'
            }
            return jsonify(response, 400)


@views.route("/CompanyDash/deleteProfile", methods=['DELETE'])
def company_dash_delete_profile():
    if request.method == 'DELETE':
        # Get logged-in user:
        user_key = auth.decode_token(request.headers['tok'])

        if user_key == -1:
            response = {
                'status': 'fail',
                'message': 'Invalid or missing token'
            }
            return jsonify(response, 403)

        # Delete all relevant data:
        try:
            contracts = Contracts.query.filter_by(CompID=user_key).all()
            for row in contracts:
                Applications.query.filter_by(ContractID=row.ContractID).delete()
                PrefLang.query.filter_by(ContractID=row.ContractID).delete()
                db.session.commit()
            Contracts.query.filter_by(CompID=user_key).delete()
            db.session.commit()
            Blocked.query.filter_by(CompID=user_key).delete()
            db.session.commit()
            Company.query.filter_by(CompID=user_key).delete()
            db.session.commit()
            response = {
                'status': 'success',
                'message': 'Successfully deleted.'
            }
            return jsonify(response, 200)
        except:
            response = {
                'status': 'fail',
                'message': 'Database error.'
            }
            return jsonify(response, 400)


@views.route("/CompanyDash/addContract", methods=['GET', 'POST'])
def company_dash_add_contract():
    if request.method == 'POST':
        post = request.get_json()

        # Save data of new contract
        new_contractDescr = post.get('contractDescr')
        new_contractVal = post.get('contractVal')
        new_contractLen = post.get('contractLen')
        new_prefLang = post.get('prefLang')
        new_location = post.get('location')

        # Get logged-in user:
        user_key = auth.decode_token(request.headers['tok'])

        # Check if user is valid
        if user_key == -1:
            response = {
                'status': 'fail',
                'message': 'Invalid or missing token'
            }
            return jsonify(response, 403)

        checker = Contracts.query.filter_by(Length=new_contractLen, Location=new_location, DatePost=date.today(),
                                            Value=new_contractVal, Descript=new_contractDescr, Status='Open',
                                            CompID=user_key).first()

        if checker is None:
            # Add contract:
            try:
                contract = Contracts(Length=new_contractLen, Location=new_location, DatePost=date.today(),
                                     Value=new_contractVal, Descript=new_contractDescr, Status='Open',
                                     CompID=user_key)
                db.session.add(contract)
                db.session.commit()

                contract_id = Contracts.query.filter_by(Length=new_contractLen, Location=new_location,
                                                        DatePost=date.today(),
                                                        Value=new_contractVal, Descript=new_contractDescr,
                                                        Status='Open',
                                                        CompID=user_key).one()

                # Add languages to table:
                for lang in new_prefLang:
                    prefLang = PrefLang(ContractID=contract_id.ContractID, Language=lang["name"])
                    db.session.add(prefLang)
                    db.session.commit()

                response = {
                    'status': 'success',
                    'message': 'Successfully added contract.'
                }
                return jsonify(response, 200)
            except:
                response = {
                    'status': 'fail',
                    'message': 'Database error.'
                }
                return jsonify(response, 400)
        else:
            response = {
                'status': 'fail',
                'message': 'Duplicate contract'
            }
            return jsonify(response, 403)


#####################################################
#               Developer Dashboard                 #
#####################################################
@views.route("/DeveloperDash", methods=['POST', 'GET'])
def developer_dash():
    if request.method == 'GET':
        # Get logged-in user:
        user_key = auth.decode_token(request.headers['tok'])

        if user_key == -1:
            response = {
                'status': 'fail',
                'message': 'Invalid or missing token'
            }
            return jsonify(response, 403)

        # Send all data to dashboard:
        try:
            dev = Developers.query.filter_by(DevID=user_key).first()
            contracts = Contracts.query.filter_by(Status='Open').all()
            contract_list = dev_contracts_to_list(contracts, user_key)

            pending = Applications.query.filter_by(DevID=user_key, ApplyStatus='Pending').all()
            accept = Applications.query.filter_by(DevID=user_key, ApplyStatus='Accepted').all()

            pending_list = applicants_list(pending)
            accept_list = applicants_list(accept)

            money_made = 0
            for i in range(len(accept_list)):
                money_made += accept_list[i]['Value']

            languages = Experience.query.filter_by(DevID=user_key).all()
            lang_list = []
            for row in languages:
                case = {'name': row.Language}
                lang_list.append(case)
            response = {
                'developerDetails': {'Username': dev.Username, 'Email': dev.Email, 'Experience': dev.Experience,
                                     'Status': dev.Status, 'UserAvatar': dev.UserAvatar, 'Languages': lang_list,
                                     'MoneyMade': money_made},
                'contracts_dictionary': contract_list,
                'PendingApplications': pending_list,
                'AcceptedApplications': accept_list,
            }
            return jsonify(response, 200)
        except:
            response = {
                'status': 'fail',
                'message': 'Database error.'
            }
            return jsonify(response, 400)

    if request.method == 'POST':
        post = request.get_json()

        user_key = auth.decode_token(request.headers['tok'])

        if user_key == -1:
            response = {
                'status': 'fail',
                'message': 'Invalid or missing token'
            }
            return jsonify(response, 403)

        if post.get('operation') == 1:
            # Apply
            try:
                contract_id = post.get('id')
                comp = Contracts.query.filter_by(ContractID=contract_id).one()
                if Applications.query.filter_by(DevID=user_key, ContractID=contract_id).first() is not None:
                    response = {
                        'status': 'failed',
                        'message': 'Already applied'
                    }
                    return jsonify(response, 200)
                apply = Applications(ApplyStatus='Pending', CompID=comp.CompID, DevID=user_key, ContractID=contract_id)
                db.session.add(apply)
                db.session.commit()
                response = {
                    'status': 'success',
                    'message': 'Successfully applied'
                }
                return jsonify(response, 200)
            except:
                response = {
                    'status': 'fail',
                    'message': 'Database error'
                }
                return jsonify(response, 404)
        elif post.get('operation') == 0:
            # Block
            try:
                company_name = post.get('company')
                comp = Company.query.filter_by(CompanyName=company_name).one()
                block = Blocked(CompID=comp.CompID, DevID=user_key)
                db.session.add(block)
                db.session.commit()
                response = {
                    'status': 'success',
                    'message': 'Successfully applied'
                }
                return jsonify(response, 200)
            except:
                response = {
                    'status': 'fail',
                    'message': 'Database error'
                }
                return jsonify(response, 404)


@views.route("/DeveloperDash/profileEdit", methods=['GET', 'PUT'])
def developer_dash_profile_edit():
    if request.method == 'GET':
        # Get logged-in user:
        user_key = auth.decode_token(request.headers['tok'])

        # Check if user is valid
        if user_key == -1:
            response = {
                'status': 'fail',
                'message': 'Invalid or missing token'
            }
            return jsonify(response, 403)

        dev = Developers.query.filter_by(DevID=user_key).one()

        # Send data of user in response:
        response = {
            'Username': dev.Username,
            'Email': dev.Email,
            'Status': dev.Status,
            'Experience': dev.Experience,
            'Avatar': dev.UserAvatar,
        }
        return jsonify(response, 200)

    elif request.method == 'PUT':
        put = request.get_json()

        # Save new data to be inserted:
        dev_name = put.get('Username')
        dev_email = put.get('Email')
        dev_status = put.get('Status')
        dev_experience = put.get('Experience')
        dev_avatar = put.get('Avatar')
        dev_languages = put.get('Languages')

        # default avatar
        if dev_avatar == "" or dev_avatar is None:
            dev_avatar = "https://us.123rf.com/450wm/asmati/asmati2005/asmati200500405/147126493-user-avatar" \
                         "-illustration-anonymous-sign-white-icon-with-gray-dropped-limitless-shadow-on-green-to-bl" \
                         ".jpg?ver=6 "

        # Get logged-in user and update data:
        try:
            # Get logged-in user:
            user_key = auth.decode_token(request.headers['tok'])
            # Check if user is valid
            if user_key == -1:
                response = {
                    'status': 'fail',
                    'message': 'Invalid or missing token'
                }
                return jsonify(response, 403)
            dev = Developers.query.filter_by(DevID=user_key).one()
            dev.Username = dev_name
            dev.Email = dev_email
            dev.Status = dev_status['name']
            dev.Experience = dev_experience
            dev.UserAvatar = dev_avatar

            db.session.commit()

            Experience.query.filter_by(DevID=user_key).delete()
            db.session.commit()
            for result in dev_languages:
                add_lang = Experience(DevID=user_key, Language=result['name'])
                db.session.add(add_lang)
                db.session.commit()

            response = {
                'status': 'success',
                'message': 'Successfully updated.'
            }
            return jsonify(response, 200)
        except:
            response = {
                'status': 'fail',
                'message': 'Database error.'
            }
            return jsonify(response, 400)


@views.route("/DeveloperDash/deleteProfile", methods=['DELETE'])
def developer_dash_delete_profile():
    if request.method == 'DELETE':
        # Get logged-in user:
        user_key = auth.decode_token(request.headers['tok'])

        # Check if user is valid
        if user_key == -1:
            response = {
                'status': 'fail',
                'message': 'Invalid or missing token'
            }
            return jsonify(response, 403)
        else:
            try:
                Applications.query.filter_by(DevID=user_key).delete()
                Experience.query.filter_by(DevID=user_key).delete()
                db.session.commit()
                Blocked.query.filter_by(DevID=user_key).delete()
                db.session.commit()
                Developers.query.filter_by(DevID=user_key).delete()
                db.session.commit()
                response = {
                    'status': 'success',
                    'message': 'Successfully deleted.'
                }
                return jsonify(response, 200)
            except:
                response = {
                    'status': 'fail',
                    'message': 'Database error.'
                }
                return jsonify(response, 400)


def contracts_to_dict(contracts):
    i = 1
    contr_dicts = {}
    for row in contracts:
        company = Company.query.filter_by(CompID=row.CompID).one()
        lang_list = []
        lang = PrefLang.query.filter_by(ContractID=row.ContractID).all()
        for result in lang:
            lang_list.append(result.Language)
        contr_dicts[i] = {'ContractID': row.ContractID, 'Length': row.Length, 'Location': row.Location,
                          'DatePost': str(row.DatePost), 'Value': row.Value, 'Descript': row.Descript,
                          'PrefLang': lang_list, 'Status': row.Status, 'CompanyName': company.CompanyName,
                          'CompanyEmail': company.Email, 'CompanyLogo': company.Logo}
        i = i + 1
    return contr_dicts


def applicants_list(applications):
    appli_dicts = []
    for row in applications:
        company = Company.query.filter_by(CompID=row.CompID).one()
        contrs = Contracts.query.filter_by(ContractID=row.ContractID).one()
        lang_list = []
        lang = Experience.query.filter_by(DevID=row.DevID).all()
        for result in lang:
            lang_list.append(result.Language)
        appli_dicts.append({'ContractID': contrs.ContractID, 'Length': contrs.Length, 'Location': contrs.Location,
                          'DatePost': str(contrs.DatePost), 'Value': contrs.Value, 'Descript': contrs.Descript,
                          'LangExp': lang_list, 'Status': contrs.Status, 'CompanyName': company.CompanyName,
                          'CompanyEmail': company.Email, 'CompanyLogo': company.Logo})
    return appli_dicts


def dev_contracts_to_list(contracts, dev_id):
    i = 1
    contract_list = []
    for row in contracts:
        company_id = row.CompID

        # skip blocked companies
        if Blocked.query.filter_by(DevID=dev_id, CompID=company_id).first() is not None or \
                Applications.query.filter_by(DevID=dev_id, ContractID=row.ContractID).first() is not None:
            continue
        company = Company.query.filter_by(CompID=row.CompID).one()
        lang_list = []
        lang = PrefLang.query.filter_by(ContractID=row.ContractID).all()

        for result in lang:
            case = {'name': result.Language}
            lang_list.append(case)

        contract_list.append({'ContractID': row.ContractID, 'Length': row.Length, 'Location': row.Location,
                              'DatePost': str(row.DatePost), 'Value': row.Value, 'Descript': row.Descript,
                              'PrefLang': lang_list, 'Status': row.Status, 'CompanyName': company.CompanyName,
                              'CompanyEmail': company.Email, 'CompanyLogo': company.Logo})
        i = i + 1
    return contract_list
