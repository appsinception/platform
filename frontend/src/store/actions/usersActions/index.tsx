import * as usersActions from "./constants";


export function SignIn(data: {token: string, user: any}) {
  return {
    type: usersActions.SIGN_IN,
    payload: data,
  };
}
export function SignUp(data: {token: string, user: any}) {
  return {
    type: usersActions.SIGN_UP,
    payload: data,
  };
}