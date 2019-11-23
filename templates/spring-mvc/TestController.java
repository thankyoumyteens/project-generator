package %BASE_PACKAGE.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
@RequestMapping("/home")
public class TestController {

    @RequestMapping("/index")
    @ResponseBody
    public String index() {
        return "ok";
    }
}
