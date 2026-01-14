INSERT INTO [Push].[SimulatedTransactions] 
    (CellPhoneNumber, Device, [State], CreateUser)
VALUES 
    ('911111111', 'Samsung Galaxy S23', 1, 'TR11439'),
    ('922222222', 'Google Pixel 8', 0, 'TR11439'),
    ('933333333', 'Huawei P40', 1, 'TR11439');

SELECT * FROM [Push].[SimulatedTransactions]