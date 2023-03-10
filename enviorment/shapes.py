#Normal shpaes of the pieces
class Shape:
    
    S = [[
        '011',
        '110'],
        [
        '100',
        '110',
        '010']]

    Z = [[
        '110',
        '011'],
        [
        '01',
        '11',
        '10']]

    I = [[
        '1',
        '1',
        '1',
        '1'],
        [
        '11110']]

    O = [[
        '11',
        '11']]

    J = [[
        '100',
        '111'],
        [
        '11',
        '10',
        '10'],
        [
        '111',
        '001'],
        [
        '01',
        '01',
        '11']]

    L = [[
        '001',
        '111'],
        [
        '10',
        '10',
        '11'],
        [
        '111',
        '100'],
        [
        '11',
        '01',
        '01']]

    T = [[
        '010',
        '111'],
        [
        '10',
        '11',
        '10'],
        [
        '111',
        '010'],
        [
        '01',
        '11',
        '01']]
    
    ALL = [I, O, T, J, L, S, Z]
    COLORS = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]