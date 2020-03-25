from flask import Blueprint
from flask import jsonify

from app.domain.model.portfolio.portfolio_type import PortfolioType
from app.domain.model.available_strategy import AvailableStrategy


bp = Blueprint('backtester', __name__)


@bp.route('/get_available_strategies')
def get_available_strategies():
    lst = list(map(lambda x: x.value, AvailableStrategy))
    return jsonify(lst)


@bp.route('/get_ptf_type')
def get_ptf_type():
    lst = list(map(lambda x: x.value, PortfolioType))
    return jsonify(lst)
