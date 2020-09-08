pragma solidity 0.5.17;

contract Registrar {

    mapping (address => string) names;
    mapping (string => address) addresses;
    mapping (address => address) linked_list;

    event NameRegistered(address _address, string _name);
    event NameUnregistered(address _address);

    function registerName(string memory _name) public {
        require(bytes(_name).length > 0);
        require(bytes(names[msg.sender]).length == 0);
        names[msg.sender] = _name;
        if (addresses[_name] == address(0)) {
            addresses[_name] = msg.sender;
        }
        else {
            address next = addresses[_name];
            while (true) {
                if (linked_list[next] == address(0))
                    break;
                next = linked_list[next];
            }
            linked_list[next] = msg.sender;
        }
        emit NameRegistered(msg.sender, _name);
    }

    function unregisterName() public {
        string memory name = names[msg.sender];
        require(bytes(name).length > 0);
        address next = addresses[name];
        if (next == msg.sender) {
            address ll_ms = linked_list[msg.sender];
            if (ll_ms == address(0))
                //Target element is only element in the list
                delete addresses[name];
            else {
                //Target element is the first element in the list
                addresses[name] = ll_ms;
                delete linked_list[msg.sender];
            }
        }
        else {
            address tmp = linked_list[next];
            while (tmp != msg.sender) {
                next = tmp;
                tmp = linked_list[next];
            }
            tmp = linked_list[msg.sender];
            if (tmp == address(0))
                //Target element is the last element in the list
                linked_list[next] = tmp;
            else {
                //Target element is in the middle of the list
                linked_list[next] = tmp;
                delete linked_list[msg.sender];
            }
        }
        emit NameUnregistered(msg.sender);
        delete names[msg.sender];
    }

    function getAddresses(string memory _name) view public returns(address [] memory) {
        if (addresses[_name] == address(0)) {
            address [] memory addrs = new address[](0);
            return addrs;
        }
        if (linked_list[addresses[_name]] == address(0)) {
            address [] memory addrs = new address[](1);
            addrs[0] = addresses[_name];
            return addrs;
        }
        else {
            uint256 length = 1;
            address next = addresses[_name];
            while (linked_list[next] != address(0)) {
                length = length + 1;
                next = linked_list[next];
            }
            address [] memory addrs = new address[](length);
            addrs[0] = addresses[_name];
            next = addresses[_name];
            for(uint256 i = 1; i < length; i++) {
                addrs[i] = linked_list[next];
                next = linked_list[next];
            }
            return addrs;
        }
    }

    function getName(address _address) view public returns(string memory) {
        return names[_address];
    }
}
