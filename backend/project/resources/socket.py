from ..model import *
from flask_restplus import Resource, fields, Namespace
from flask import url_for, redirect, request, abort, make_response , jsonify , session, flash
from project import app, db, rest_api
from datetime import datetime
from sqlalchemy import or_, asc, desc
from ..model.guest_message import GuestMessage
from project.utils import token_required, token_optional
from project.helpers import *
from project.lang.fa import *
from definitions import SITE_PREFIX, COINS_BASE_PRICE, GEMS_BASE_PRICE
import math

socket_ns = Namespace('socket')

socket_auction_model = socket_ns.model('SocketAuction', {
    "auctionId":fields.Integer()
})

socket_auction_status_model = socket_ns.model('SocketAuctionStatus', {
    "auctionId":fields.Integer(),
    "bidPrice":fields.Integer(),
    "name":fields.String(),
    "avatar":fields.String(),
})

socket_auction_users_model = socket_ns.model('SocketAuctionUsers', {
    "auctionId":fields.Integer(),
    "row":fields.Integer(),
    "name":fields.String(),
    "bidPrice":fields.Integer(),
    "avatar":fields.String(),
    "level":fields.Integer(),
})

socket_error_model = socket_ns.model('SocketError', {
    "auctionId":fields.Integer(),
    "message":fields.String(),
    "reason":fields.String(),
    "status":fields.Integer(),
})

socket_failed_model = socket_ns.model('SocketFailed', {
    "error":fields.Nested(socket_error_model),
})

socket_auction_reset_model = socket_ns.model('SocketAuctionReset', {
    "auctionId":fields.Integer(),
    "heartbeat":fields.Integer(),
})

socket_auction_bids_model = socket_ns.model('SocketAuctionBids', {
    "auctionId":fields.Integer(),
    "bids":fields.Integer(),
})

socket_auction_sync_model = socket_ns.model('SocketAuctionSync', {
    "auctionId":fields.Integer(),
    "message":fields.String(),
})

socket_auction_fenito_model = socket_ns.model('SocketAuctionFinish', {
    "auctionId":fields.Integer(),
    "error.message":fields.String(),
})

socket_auction_winner_model = socket_ns.model('SocketAuctionWinner', {
    "auctionId":fields.Integer(),
    "name":fields.String(),
    "avatar":fields.String(),
    "bidPrice":fields.Integer(),
})

@socket_ns.route('/connect')
class connect(Resource):
    def post(self):
        pass
    @socket_ns.response(200, 'client successfully connected to the server socket provider')
    def get(self):
        pass

@socket_ns.route('/keepalive')
class keepalive(Resource):
    def post(self):
        pass
    @socket_ns.response(200, 'keep alive client and server websocket connection every 1 second')
    def get(self):
        pass

@socket_ns.route('/join_public')
class join_public(Resource):
    @socket_ns.doc('join client to the public auction channel.', body=socket_auction_model, validate=True)
    def post(self):
        pass

@socket_ns.route('/join_private')
class join_private(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @socket_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @socket_ns.doc('join client to the private channel.',parser=parser, validate=True)
    def post(self):
        pass

@socket_ns.route('/joined')
class joined(Resource):
    @socket_ns.response(200, 'client successfully joined specific channel')
    def get(self):
        pass

@socket_ns.route('/leave')
class leave(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @socket_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @socket_ns.doc('leave client from the private and public channel.',parser=parser, body=socket_auction_model, validate=True)
    @socket_ns.response(200, 'client successfully leaved channel')
    def post(self):
        pass

@socket_ns.route('/leaved')
class leaved(Resource):
    @socket_ns.response(200, 'client successfully leaved specific channel')
    def get(self):
        pass

@socket_ns.route('/getStatus')
class getStatus(Resource):
    @socket_ns.doc('get auction status from auction public channel.', body=socket_auction_model, validate=True)
    def post(self):
        pass

@socket_ns.route('/status')
class status(Resource):
    @socket_ns.response(200, 'get auction status from the channel',socket_auction_status_model)
    def get(self):
        pass

@socket_ns.route('/getUsers')
class getUsers(Resource):
    @socket_ns.doc('get auction users from auction public channel.', body=socket_auction_model, validate=True)
    def post(self):
        pass

@socket_ns.route('/users')
class users(Resource):
    @socket_ns.response(200, 'get auction users from the channel',socket_auction_users_model)
    def get(self):
        pass

@socket_ns.route('/failed')
class failed(Resource):
    @socket_ns.response(200, 'failed operation',socket_failed_model)
    def get(self):
        pass

@socket_ns.route('/failed')
class failed(Resource):
    @socket_ns.response(200, 'failed operation',socket_failed_model)
    def get(self):
        pass

@socket_ns.route('/bid')
class bid(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @socket_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @socket_ns.doc('handle bid for auction base on public channel.', parser=parser, body=socket_auction_model, validate=True)
    def post(self):
        pass

@socket_ns.route('/reset')
class reset(Resource):
    @socket_ns.response(200, 'reset client timer for all users on auction channel',socket_auction_reset_model)
    def get(self):
        pass

@socket_ns.route('/bids')
class bids(Resource):
    @socket_ns.response(200, 'send remained bids to private user auction channel',socket_auction_bids_model)
    def get(self):
        pass

@socket_ns.route('/iceAge')
class iceAge(Resource):
    @socket_ns.response(200, 'send auction timer before 60 seconds',socket_auction_reset_model)
    def get(self):
        pass

@socket_ns.route('/holliDay')
class holliDay(Resource):
    @socket_ns.response(200, 'send auction timer between 60 and 10 seconds',socket_auction_reset_model)
    def get(self):
        pass

@socket_ns.route('/hotSpot')
class hotSpot(Resource):
    @socket_ns.response(200, 'send auction timer between 10 and -1 seconds',socket_auction_reset_model)
    def get(self):
        pass

@socket_ns.route('/zeroTime')
class zeroTime(Resource):
    @socket_ns.response(200, 'sync auction bids between -1 and -3 seconds',socket_auction_sync_model)
    def get(self):
        pass

@socket_ns.route('/feniTto')
class feniTto(Resource):
    @socket_ns.response(200, 'send finished auction without any bids',socket_auction_fenito_model)
    def get(self):
        pass

@socket_ns.route('/winner')
class winner(Resource):
    @socket_ns.response(200, 'broadcast auction winner to all clients',socket_auction_winner_model)
    def get(self):
        pass
