def transfer(self, from_account_id, to_account_id, amount):
        """Transfer funds between two accounts and track the operation"""
        with tracer.start_as_current_span("transfer_operation") as span:
            span.set_attribute("from_account_id", from_account_id)
            span.set_attribute("to_account_id", to_account_id)
            span.set_attribute("amount", amount)
            try:
                if from_account_id == to_account_id:
                    raise ValueError("Cannot transfer funds to the same account.")

                from_account = self.get_account(from_account_id)
                to_account = self.get_account(to_account_id)

                # Withdraw from the source account
                from_account.withdraw(amount)

                # Deposit to the target account
                to_account.deposit(amount)

                # Record the transfer operation metric
                self.transfer_counter.add(1, attributes={"from_account_id": from_account_id, "to_account_id": to_account_id})

                span.set_status(Status(StatusCode.OK))
                span.set_attribute("new_balance_from", from_account.get_balance())
                span.set_attribute("new_balance_to", to_account.get_balance())

                return (from_account.get_balance(), to_account.get_balance())
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise