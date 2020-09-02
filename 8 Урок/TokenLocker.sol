pragma solidity ^0.5.17;


contract IEC20 {
    function transferFrom(address _from, address _to, uint256 _amount) external;
    event Transfer(
        address indexed from,
        address indexed to,
        uint256 value
        );

}
contract TokenLocker {
    IEC20 public tokenAddress;

    event TokenLocked(address sender, uint256 amount);

    constructor (IEC20 _token) public {
        tokenAddress = _token;
    }

    function relay(uint _amount) external {
       tokenAddress.transferFrom(msg.sender, address(this), _amount);

       emit TokenLocked(msg.sender, _amount);
    }
}