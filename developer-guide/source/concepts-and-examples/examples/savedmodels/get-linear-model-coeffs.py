def get_model_coefficients(project, saved_model_id, version_id):
    """
    Returns a dictionary with key="coefficient name" and value=coefficient
    """

    model = project.get_saved_model(saved_model_id)
    if version_id is None:
        version_id = model.get_active_version().get('id')
    details = model.get_version_details(version_id)
    details_lr = details.details.get('iperf', {}).get('lmCoefficients', {})
    rescaled_coefs = details_lr.get('rescaledCoefs', [])
    variables = details_lr.get('variables',[])
    coef_dict = {var: coef for var, coef in zip(variables, rescaled_coefs)}
    if len(coef_dict)==0:
        print(f"Model {saved_model_id} and version {version_id} does not have coefficients")
    return coef_dict