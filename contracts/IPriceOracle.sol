
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IPriceOracle {
    function getPrice(string calldata symbol) external view returns (uint256);
}
