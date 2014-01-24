from mock import Mock, call
from sure import expect

import guesser


def args_from_call_list(call_list):
    # Each call object is a tuple. The first item is the call args
    return [c[0][0] for c in call_list]


def test_guessing_without_start():

    def check_if_book_exists(book_id):
        if book_id < 27:
            return True
        return False

    fake_func = Mock(side_effect=check_if_book_exists)

    result = guesser.guess(fake_func)
    result.should.equal(26)
    expect(args_from_call_list(fake_func.call_args_list)).should.equal(
        [10, 20, 40, 30, 25, 28, 27, 26]
    )


def test_guessing_with_high_start():

    def check_if_book_exists(book_id):
        if book_id < 27:
            return True
        return False

    fake_func = Mock(side_effect=check_if_book_exists)

    result = guesser.guess(fake_func, start=50)
    result.should.equal(26)
    args_from_call_list(fake_func.call_args_list).should.equal(
        [50, 25, 38, 32, 29, 27, 26],
    )


def test_guessing_with_low_start():

    def check_if_book_exists(book_id):
        if book_id < 27:
            return True
        return False

    fake_func = Mock(side_effect=check_if_book_exists)
    result = guesser.guess(fake_func, start=2)
    result.should.equal(26)
    args_from_call_list(fake_func.call_args_list).should.equal(
        [2, 4, 8, 16, 32, 24, 28, 26, 27],
    )


def test_guessing_with_correct_start():

    def check_if_book_exists(book_id):
        if book_id < 27:
            return True
        return False

    fake_func = Mock(side_effect=check_if_book_exists)
    result = guesser.guess(fake_func, start=26)
    result.should.equal(26)
    fake_func.call_count.should.equal(7)
    args_from_call_list(fake_func.call_args_list).should.equal(
        [26, 52, 39, 33, 30, 28, 27],
    )


def test_guessing_with_just_above_start():

    def check_if_book_exists(book_id):
        if book_id < 27:
            return True
        return False

    fake_func = Mock(side_effect=check_if_book_exists)
    result = guesser.guess(fake_func, start=27)
    result.should.equal(26)
    args_from_call_list(fake_func.call_args_list).should.equal(
        [27, 13, 20, 24, 26],
    )


def test_guessing_with_scale_factor():

    def check_if_book_exists(book_id):
        if book_id < 743:
            return True
        return False

    fake_func = Mock(side_effect=check_if_book_exists)
    result = guesser.guess(fake_func, start=50, scale_factor=10)
    result.should.equal(742)
    args_from_call_list(fake_func.call_args_list).should.equal(
        [50, 500, 5000, 2750, 1625, 1063, 782, 641, 712, 747, 730, 739, 743, 741, 742]
    )


def test_func_with_other_args():

    def check_if_book_exists(book_id, author_name, sale_count=0):
        if book_id < 27:
            return True
        return False

    fake_func = Mock(side_effect=check_if_book_exists)
    result = guesser.guess(fake_func, "Mark Twain", sale_count=3, start=50, scale_factor=10)
    result.should.equal(26)
    list(fake_func.call_args_list).should.equal([
        call(50, 'Mark Twain', sale_count=3),
        call(25, 'Mark Twain', sale_count=3),
        call(38, 'Mark Twain', sale_count=3),
        call(32, 'Mark Twain', sale_count=3),
        call(29, 'Mark Twain', sale_count=3),
        call(27, 'Mark Twain', sale_count=3),
        call(26, 'Mark Twain', sale_count=3),
    ])
