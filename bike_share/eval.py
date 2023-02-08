import sklearn
import sklearn.metrics

def regression_results(x, y_true, model):

    y_pred = model.predict(x)

    r2 = sklearn.metrics.r2_score(y_true, y_pred)
    mse = sklearn.metrics.mean_squared_error(y_true, y_pred)

    print(f"R^2: {round(r2,4)}")
    print(f"MSE: {round(mse,4)}")


def get_regression_info(model):
    colnames = model.feature_names_in_
    # zip with coeffs (numbers) being the first component
    # so sort will sort w.r.t it preferrably
    col_coeffs = zip(model.coef_, colnames)
    col_coeffs_sorted = sorted(col_coeffs)
    print(f"Intercept: {model.intercept_}")
    print(f"Top-5 coeffs: {col_coeffs_sorted[:10]}")
    return col_coeffs_sorted
