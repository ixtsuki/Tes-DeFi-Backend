
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IDeFiVault {
    function deposit(address user, string calldata asset, uint256 amount) external;
    function borrow(address user, string calldata asset, uint256 amount) external;
    function getHealth(address user) external view returns (uint256 ltv);
}
