import {
    Button,
    Drawer,
    DrawerBody,
    DrawerCloseButton,
    DrawerContent,
    DrawerFooter,
    DrawerHeader,
    DrawerOverlay,
    createDisclosure,
    Input,
    InputLeftAddon,
    InputRightAddon,
    InputGroup
} from "@hope-ui/solid";

function MenuDrawer() {
    const { isOpen, onOpen, onClose } = createDisclosure();

    return (
        <>
            <Button onClick={onOpen}>Menu</Button>
            <Drawer opened={isOpen()} placement="right" onClose={onClose}>
                <DrawerOverlay />
                <DrawerContent>
                    <DrawerCloseButton />
                    <DrawerHeader>Control The Table</DrawerHeader>

                    <DrawerBody>
                        <InputGroup>
                            <InputLeftAddon>Width:</InputLeftAddon>
                            <Input placeholder="12" />
                            <InputRightAddon>hours</InputRightAddon>
                        </InputGroup>
                        <InputGroup>
                            <InputLeftAddon>Height:</InputLeftAddon>
                            <Input placeholder="20" />
                            <InputRightAddon>days</InputRightAddon>
                        </InputGroup>
                    </DrawerBody>

                    
                </DrawerContent>
            </Drawer>
        </>
    );
}

export default MenuDrawer;
