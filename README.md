About
=====

Three tools to monitor Ripple transactions.<br />
You can monitor offers, payments, and trustsets.<br />

That's a first draft ;)<br />
I will try to merge the 3 scripts to have only one tool ;)<br />

The code is not really cleaned and may be buggy!<br />
Do not hesitate to contribute and/or to report bugs ;)<br />



Howto
=====

Monitor offers
--------------

    $ python monitor-offers.py wss://s1.ripple.com:51233/
    [2013-06-28 20:45:50]{OfferCreate-310} r3JhfnpuMQefFtv1qHTgMeEsTsXXsfuLwc made offer to give 1,020 XRP for 20 CAD
    [2013-06-28 20:46:40]{OfferCreate-123} rG6yfm6M8oVTuECSmiCysrnsp5eq5f5mNR made offer to give 16,771.17736 XRP for 263.98 USD
    [2013-06-28 20:46:50]{OfferCreate-270} rwhjDDbqyGBjCFQHMoJy8ZtPTuZWZPL1aM made offer to give 516 XRP for 6 GBP
    [2013-06-28 20:48:30]{OfferCreate-271} rwhjDDbqyGBjCFQHMoJy8ZtPTuZWZPL1aM made offer to give 1.26 EUR for 142.38 XRP
    [2013-06-28 20:49:30]{OfferCreate-124} rG6yfm6M8oVTuECSmiCysrnsp5eq5f5mNR made offer to give 16,768.944 XRP for 258.78 USD
    [2013-06-28 20:50:00]{OfferCancel-1264} rNAAy9xnjuU6McAjVFtMyFbDNKzTXQ9wbV has cancelled offer #1264
    [2013-06-28 20:50:00]{OfferCreate-44} rwVLfZK3Ncjd72QahqZRwWv8rcwtQDRAcf made offer to give 31,125 XRP for 5 BTC
    [2013-06-28 20:50:30]{OfferCancel-310} r3JhfnpuMQefFtv1qHTgMeEsTsXXsfuLwc has cancelled offer #310

Monitor payments
----------------

    $ python monitor-payments.py wss://s1.ripple.com:51233/
    [2013-06-28 20:32:00]{Payment} rUSdkSimxiENqKyrExauLatszy7mnG83fH has sent 6 XRP to rpyUV8W6XRvss6SBkAS8PyzGwMsSDxgNXW
    [2013-06-28 20:32:10]{Payment} rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B has sent 50,000 USD to rrpNnNLKrartuEqfJGpqyDwPj1AFPg9vn1
    [2013-06-28 20:32:50]{Payment} rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B has sent 300 BTC to rrpNnNLKrartuEqfJGpqyDwPj1AFPg9vn1
    [2013-06-28 20:33:00]{Payment} rUSdkSimxiENqKyrExauLatszy7mnG83fH has sent 6 XRP to rpyUV8W6XRvss6SBkAS8PyzGwMsSDxgNXW
    [2013-06-28 20:33:20]{Payment} rpyUV8W6XRvss6SBkAS8PyzGwMsSDxgNXW has sent 12 XRP to rUSdkSimxiENqKyrExauLatszy7mnG83fH
    [2013-06-28 20:33:40]{Payment} rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B has sent 250,000 XRP to rrpNnNLKrartuEqfJGpqyDwPj1AFPg9vn1
    [2013-06-28 20:33:50]{Payment} rHhbv3wQDvR8CWmMPVvt1q2xKVXoi98ZHV has sent 105 XRP to rEd5kLvLK5NbyzgCKVmHN3TeM6TcSKHahG

Monitor trustsets
-----------------

    $ python monitor-trustsets.py wss://s1.ripple.com:51233/
    [2013-06-28 20:25:10] rUAMuQTfVhbfqUDuro7zzy4jj4Wq57MPTj has trusted rLJe38XtVZt6VKjKsSngHDd4kPbT49EuRZ for 10 UAM
    [2013-06-28 20:25:20] rbvFfuUysurzPHq5kgs53A16j5svbFxgv has trusted rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh for 0 USD
    [2013-06-28 20:29:00] rNn5Fe8L5STcnykUrEkoFmQ5jdtrXaSsw7 has trusted rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B for 50 BTC
    [2013-06-28 20:31:00] rBqupmyHgKpCVxuz1eyTRuAyJi3nj714EP has trusted rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B for 20 USD
    [2013-06-28 20:31:20] rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh has trusted rbvFfuUysurzPHq5kgs53A16j5svbFxgv for 10 ZSX
    [2013-06-28 20:31:40] rrpNnNLKrartuEqfJGpqyDwPj1AFPg9vn1 has trusted rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B for 100,000 USD

You need python and websocket-client installed ;)


Bugs
====

Known bugs
----------

Fatal bug in the SSL part of the websocket-client library? (reported)
[Errno 8] _ssl.c:1359: EOF occurred in violation of protocol

