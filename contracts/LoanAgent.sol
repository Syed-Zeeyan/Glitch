// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LoanAgent {
    event LoanApproved(address indexed borrower, uint256 amount);

    function approveLoan(address borrower, uint256 amount) public {
        // In real version, you’d store or verify this
        emit LoanApproved(borrower, amount);
    }
}
