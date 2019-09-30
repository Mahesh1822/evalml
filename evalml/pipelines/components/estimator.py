from sklearn.ensemble import RandomForestClassifier as SKRandomForestClassifier
from sklearn.ensemble import RandomForestRegressor as SKRandomForestRegressor
from sklearn.linear_model import LinearRegression as SKLinearRegression
from sklearn.linear_model import LogisticRegression as LogisticRegression
from skopt.space import Integer, Real
from xgboost import XGBClassifier

from .component_base import ComponentBase
from .component_types import ComponentTypes


class Estimator(ComponentBase):
    def __init__(self, name, component_type, hyperparameters=None, needs_fitting=False, component_obj=None, random_state=0):
        super().__init__(name=name, component_type=component_type, hyperparameters=hyperparameters, needs_fitting=needs_fitting,
                         component_obj=component_obj, random_state=random_state)

    def predict(self, X):
        """Make predictions using selected features.

        Args:
            X (DataFrame) : features

        Returns:
            Series : estimated labels
        """
        self._component_obj.predict(X)

    def predict_proba(self, X):
        """Make probability estimates for labels.

        Args:
            X (DataFrame) : features

        Returns:
            DataFrame : probability estimates
        """
        self._component_obj.predict_proba(X)

    def score(self, X, y, other_objectives=None):
        """Evaluate model performance

        Args:
            X (DataFrame) : features for model predictions
            y (Series) : true labels
            other_objectives (list): list of other objectives to score

        Returns:
            score, dictionary of other objective scores
        """
        self._component_obj.score(X, y)


class LogisticRegressionClassifier(Estimator):
    def __init__(self, penalty="l2", C=1.0, n_jobs=-1, random_state=0):
        self.name = "Logistic Regression Classifier"
        self.component_type = ComponentTypes.CLASSIFIER
        self.penalty = penalty
        self.C = C
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.hyperparameters = {
            "penalty": ["l2"],
            "C": Real(.01, 10),
        }
        self._component_obj = LogisticRegression(penalty=self.penalty,
                                                 C=self.C,
                                                 random_state=self.random_state,
                                                 multi_class="auto",
                                                 solver="lbfgs",
                                                 n_jobs=self.n_jobs)
        super().__init__(name=self.name, component_type=self.component_type, hyperparameters=self.hyperparameters, component_obj=self._component_obj)


class RandomForestClassifier(Estimator):
    def __init__(self, n_estimators, max_depth=None, n_jobs=-1, random_state=0):
        self.name = "Random Forest Classifier"
        self.component_type = ComponentTypes.CLASSIFIER
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.hyperparameters = {
            "n_estimators": Integer(10, 1000),
            "max_depth": Integer(1, 32),
        }
        self._component_obj = SKRandomForestClassifier(random_state=self.random_state,
                                                       n_estimators=self.n_estimators,
                                                       max_depth=self.max_depth,
                                                       n_jobs=self.n_jobs)
        super().__init__(name=self.name, component_type=self.component_type, hyperparameters=self.hyperparameters, component_obj=self._component_obj)


class XGBoostClassifier(Estimator):
    def __init__(self, eta, max_depth, min_child_weight, random_state=0):
        self.name = "XGBoost Classifier"
        self.component_type = ComponentTypes.CLASSIFIER
        self.eta = eta
        self.max_depth = max_depth
        self.min_child_weight = min_child_weight
        self.random_state = random_state
        self.hyperparameters = {
            "eta": Real(0, 1),
            "max_depth": Integer(1, 20),
            "min_child_weight": Real(1, 10),
        }
        self._component_obj = XGBClassifier(random_state=self.random_state,
                                            eta=self.eta,
                                            max_depth=self.max_depth,
                                            min_child_weight=self.min_child_weight)
        super().__init__(name=self.name, component_type=self.component_type, hyperparameters=self.hyperparameters, component_obj=self._component_obj)


class RandomForestRegressor(Estimator):
    def __init__(self, n_estimators, max_depth=None, n_jobs=-1, random_state=0):
        self.name = "Random Forest Regressor"
        self.component_type = ComponentTypes.REGRESSOR
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.hyperparameters = {
            "n_estimators": Integer(10, 1000),
            "max_depth": Integer(1, 32),
        }
        self._component_obj = SKRandomForestRegressor(random_state=self.random_state,
                                                      n_estimators=self.n_estimators,
                                                      max_depth=self.max_depth,
                                                      n_jobs=self.n_jobs)
        super().__init__(name=self.name, component_type=self.component_type, hyperparameters=self.hyperparameters, component_obj=self._component_obj)


class LinearRegressor(Estimator):
    def __init__(self, n_jobs=-1):
        self.name = "Linear Regressor"
        self.component_type = ComponentTypes.REGRESSOR
        self.hyperparameters = {}
        self._component_obj = SKLinearRegression()
        super().__init__(name=self.name, component_type=self.component_type, hyperparameters=self.hyperparameters, component_obj=self._component_obj)
